"""
Hierarchical State Machine (HSM) — documentación general

Propósito
---------
Este módulo implementa la representación en tiempo de ejecución de una
Máquina de Estados Jerárquica (HSM) usada por los componentes de IA.
Proporciona:
- Tipos de prototipos (StatePrototype, TransitionPrototype, HSMPrototype).
- Runtime (HSMInstance) que mantiene la pila activa, el blackboard y la historia
  ("deep history") de composites.
- API mínima para arrancar, actualizar y consultar el estado activo.

PD: Para efecto de ejemplificación se toma el GUARDIAN_BEHAVIOR descrito en
src/data/enemies.py

Conceptos clave
---------------
- Spec declarativa: la HSM se describe con un diccionario (spec) en
  src/data/enemies.py. El builder (ai/hsm_builder.py) transforma esa spec en
  HSMPrototype, resolviendo acciones y condiciones definidas en
  src/ai/actions.py y src/ai/conditions.py.

- StatePrototype:
  - stype: "leaf" o "composite".
  - entry/update/exit: listas de acciones (callables con firma (hinst, entity)).
  - substates: nombres relativos (no fully-qualified) para composites.
  - initial: subestado inicial (nombre relativo).
  - transitions: lista de TransitionPrototype.
  - history: "deep" | "shallow" | None (soporta restauración deep de composites).

- TransitionPrototype:
  - to: ruta destino (puede ser fully-qualified o relativa).
  - cond: función condición (hinst, entity) -> bool o None (default = siempre true).
  - priority: prioridad numérica (mayor = más prioridad).
  - cond_params: parámetros que se exponen temporalmente en blackboard durante la evaluación.
  - restore_history: si true, al entrar se restaura la historia del composite destino.

- HSMInstance (runtime):
  - active_stack: lista de rutas desde root hasta la hoja activa (p.ej. ["root", "root.EstadoVida", "root.EstadoVida.Vigilar"]).
  - blackboard: dict compartido entre acciones/condiciones; inicializado con
    `_spec_params`, `manager`, `entity`, etc.
  - history: snapshots para composites con history="deep".
  - Entradas:
    - _enter_path(path): entra en la ruta indicada, ejecutando entry actions y descendiendo por `initial` o restaurando history.
    - _exit_to_common_ancestor(target_path): ejecuta exit actions y guarda snapshots deep cuando corresponda.
  - update(entity, dt):
    - Ejecuta actions `update` desde la hoja hacia la raíz (bottom-up).
    - Evalúa transiciones hoja→raíz, exponiendo `cond_params` en `_last_transition_cond_params`.
    - Escoge la transición de mayor prioridad y aplica la transición (exit→enter).

Extensibilidad
--------------
- Añadir acciones/condiciones: registrar en `src/ai/actions.py` / `src/ai/conditions.py`.
- Para nuevas transiciones complejas, usar `_last_transition_cond_params` para pasar
  parámetros por transición y evitar hardcoding en condiciones.

Referencias rápidas en el workspace
----------------------------------
- Spec / ejemplos: src/data/enemies.py
- Builder: src/ai/hsm_builder.py
- Actions registry: src/ai/actions.py
- Conditions registry: src/ai/conditions.py
- Componente Behavior: src/ai/behavior.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

Action = Callable[[Any, Any], None]      # (hinst, entity)
Condition = Callable[[Any, Any], bool]   # (hinst, entity)

@dataclass
class TransitionPrototype:
    """
    Descripción
        CLASE: Representación de una transición en el prototipo de HSM.

    Atributos
        - to: ruta del estado destino (string).
        - cond: función condición (hinst, entity) -> bool o None.
        - priority: prioridad numérica (mayor = más prioridad).
        - cond_params: parámetros auxiliares expuestos en blackboard durante la evaluación.
        - restore_history: si true indica que al entrar se debe restaurar history del composite destino.
    """
    to: str
    cond: Optional[Condition] = None
    priority: int = 100
    cond_params: Dict[str, Any] = field(default_factory=dict)
    restore_history: bool = False


@dataclass
class StatePrototype:
    """
    Descripción
        CLASE: Prototipo de estado.

    Atributos
        - name: nombre de la clave en el spec.
        - stype: "leaf" | "composite".
        - entry, update, exit: listas de acciones (callables).
        - substates: nombres relativos de subestados.
        - initial: nombre relativo del subestado inicial.
        - transitions: lista de TransitionPrototype.
        - history: "deep" | "shallow" | None.
    """
    name: str
    stype: str = "leaf"
    entry: List[Action] = field(default_factory=list)
    update: List[Action] = field(default_factory=list)
    exit: List[Action] = field(default_factory=list)
    substates: List[str] = field(default_factory=list)
    initial: Optional[str] = None
    transitions: List[TransitionPrototype] = field(default_factory=list)
    history: Optional[str] = None


@dataclass
class HSMPrototype:
    """
    Descripción
        CLASE: Contenedor del spec construido por el builder.
    
    Atributos
        - name: nombre de la HSM.
        - params: parámetros globales del spec.
        - states: mapa de nombres a StatePrototype.
        - root: nombre del estado raíz.
    """
    name: str
    params: Dict[str, Any]
    states: Dict[str, StatePrototype]
    root: str = "root"


class HSMInstance:
    """
    Descripción
        CLASE: Instancia en ejecución de la HSM (Hierarchical State Machine).
        Representa el runtime de una máquina de estados jerárquica construida a partir
        de un prototipo generado por el builder.

    Atributos
        - prototype (HSMPrototype): prototipo de la HSM (estados, transiciones, params).
        - blackboard (Dict[str, Any]): diccionario compartido para comunicación entre
          acciones, condiciones y estados. Inicializado con la clave `_spec_params`.
        - active_stack (List[str]): pila de rutas activas desde la raíz hasta la hoja.
          Ejemplo: ["root", "root.EstadoVida", "root.EstadoVida.Atacar"].
        - history (Dict[str, List[str]]): snapshots para composites que declaran
          history="deep". La clave es el path del composite y el valor es la lista
          de subpaths activos que representan la historia.
        - (internos) `_last_transition_cond_params`, etc.: campos auxiliares usados
          durante la evaluación de transiciones.

    Responsabilidades / Métodos principales
        - _enter_path(path): entrar en la ruta indicada; ejecutar entry actions,
          descender por `initial` o restaurar deep history si procede.
        - _exit_to_common_ancestor(target_path): salir de la pila hasta el ancestro
          común con `target_path`, ejecutar exit actions y guardar snapshots de
          deep history cuando corresponda.
        - update(entity, dt): ciclo por tick que:
            1) registra `dt` y `entity` en el blackboard,
            2) ejecuta update actions desde la hoja hacia la raíz (bottom-up),
            3) evalúa transiciones hoja→raíz, selecciona la de mayor prioridad y la aplica.
        - get_active_stack(): devuelve una copia de la pila activa.
        - set_blackboard(key, val) / get_blackboard(key, default): utilidades para
          leer/escribir en el blackboard de forma explícita.

    Convenciones
        - Todas las acciones y condiciones se ejecutan con la firma (hinst, entity).
        - Las claves del blackboard que comienzan con "_" están reservadas para uso
          interno (p.ej. `_spec_params`, `_last_transition_cond_params`).
        - Las condiciones deben ser rápidas y defensivas (no propagar excepciones).
        - Las acciones deben documentar claramente qué claves del blackboard leen/escriben.
        - El campo `history` almacena lists de rutas fully-qualified relativas al composite.
        - La API del HSM evita efectos secundarios inesperados: la restauración de
          history se realiza antes de evaluar nuevas transiciones al entrar en un composite.
    """

    def __init__(self, prototype: HSMPrototype, blackboard: Optional[Dict[str, Any]] = None):
        self.prototype = prototype
        self.blackboard: Dict[str, Any] = dict(blackboard or {})
        # asegurar que los params del spec estén accesibles
        self.blackboard.setdefault("_spec_params", prototype.params)
        self.active_stack: List[str] = []
        self.history: Dict[str, List[str]] = {}
        # iniciar en root (desciende hasta hoja inicial)
        try:
            self._enter_path(self.prototype.root)
        except Exception as e:
            print(f"[HSM INIT] Error al inicializar HSM: {e}")

    # --------------------
    # Utilitarios / búsquedas
    # --------------------
    def _get_state_proto(self, path: str) -> StatePrototype:
        """
        Descripción
            MÉTODO: Resuelve una ruta a un StatePrototype aplicando heurísticas sobre
            nombres relativos y prefijos.

        Argumentos
            - path (str): ruta buscada (puede ser fully-qualified o relativa).

        Retorno
            - StatePrototype: el prototipo asociado a la ruta.

        Excepciones
            - Lanza KeyError si no existe un prototipo que corresponda a la ruta.
        """
        if path in self.prototype.states:
            return self.prototype.states[path]
        last = path.split(".")[-1]
        if last in self.prototype.states:
            return self.prototype.states[last]
        root_prefix = f"{self.prototype.root}."
        if path.startswith(root_prefix):
            alt = path[len(root_prefix):]
            if alt in self.prototype.states:
                return self.prototype.states[alt]
        raise KeyError(path)

    def _split_path(self, path: str) -> List[str]:
        """
        Descripción
            FUNCIÓN: Divide una ruta en sus segmentos por el separador '.'.

        Argumentos
            - path (str): ruta a dividir.

        Retorno
            - List[str]: lista de segmentos.
        """
        return path.split(".")

    # --------------------
    # Ejecución de acciones
    # --------------------
    def _call_actions(self, actions: List[Action], entity: Any, kind: str):
        """
        Descripción
            MÉTODO: Ejecuta una lista de acciones capturando excepciones y reportando
            errores formateados para debugging.

        Argumentos
            - actions (List[Action]): lista de callables con firma (hinst, entity).
            - entity (Any): entidad sobre la que se ejecutan las acciones.
            - kind (str): etiqueta de contexto ("ENTRY"/"UPDATE"/"EXIT") usada en logs.

        Retorno
            - None

        Notas
            - Las excepciones se capturan individualmente por acción para evitar que
              una acción fallida interrumpa la ejecución de las restantes.
        """
        for act in actions:
            try:
                act(self, entity)
            except Exception as err:
                print(f"[HSM {kind}] Error en acción {act}: {err}")

    def _call_entry_actions(self, state_path: str, entity: Any = None):
        """
        Descripción
            MÉTODO: Ejecuta las acciones de entry declaradas en el StatePrototype
            asociado a `state_path`.

        Argumentos
            - state_path (str): ruta del estado cuyo entry ejecutar.
            - entity (Any): entidad pasiva para las acciones (opcional).

        Retorno
            - None
        """
        try:
            proto = self._get_state_proto(state_path)
        except KeyError:
            return
        self._call_actions(proto.entry, entity, "ENTRY")

    def _call_update_actions(self, state_path: str, entity: Any = None):
        """
        Descripción
            MÉTODO: Ejecuta las acciones de update del StatePrototype para `state_path`.

        Argumentos
            - state_path (str): ruta del estado cuyo update ejecutar.
            - entity (Any): entidad para pasar a las acciones (opcional).

        Retorno
            - None
        """
        try:
            proto = self._get_state_proto(state_path)
        except KeyError:
            return
        self._call_actions(proto.update, entity, "UPDATE")

    def _call_exit_actions(self, state_path: str, entity: Any = None):
        """
        Descripción
            MÉTODO: Ejecuta las acciones de exit del StatePrototype para `state_path`.

        Argumentos
            - state_path (str): ruta del estado cuyo exit ejecutar.
            - entity (Any): entidad para pasar a las acciones (opcional).

        Retorno
            - None

        Notas
            - Las acciones de exit se ejecutan en el orden declarado en el prototipo.
        """
        try:
            proto = self._get_state_proto(state_path)
        except KeyError:
            return
        # ejecutar exits en orden declarado
        self._call_actions(proto.exit, entity, "EXIT")

    # --------------------
    # Entradas / salidas de estados
    # --------------------
    def _enter_path(self, path: str):
        """
        Descripción
            MÉTODO: Entra en la ruta 'path' (puede ser fully-qualified o relativa).
            Acciones realizadas (resumen secuencial):
              1) Normalizar la ruta en una lista acumulada de nodos (ancestros).
              2) Calcular el prefijo común con la pila actual (active_stack).
              3) Ejecutar exit actions de los estados que se dejarán.
              4) Para cada estado faltante, ejecutar entry actions y:
                 - Si es composite y declara history="deep" y existe snapshot en `history`,
                   restaurar dicha historia (llamando recursivamente a _enter_path).
                 - Si es composite con `initial`, descender al subestado inicial.
                 - En otro caso, simplemente añadir el estado a la pila.
              5) Terminar con la máquina en un estado hoja (si procede).

        Argumentos
            - path (str): ruta destino a la que entrar.

        Retorno
            - None

        Notas de implementación
            - La restauración de history se realiza antes de evaluar nuevas transiciones
              para garantizar que el estado restaurado tenga oportunidad de ejecutar
              sus entry/update antes de ser re-evaluado por condiciones.
        """
        parts = self._split_path(path)
        # construir la lista de rutas acumuladas: ["root", "root.X", "root.X.Y", ...] si corresponde
        accum: List[str] = []
        for i, part in enumerate(parts):
            if i == 0:
                accum.append(part)
            else:
                accum.append(f"{accum[-1]}.{part}")

        # si la ruta exacta está registrada como prototipo, usamos la cadena completa de ancestros
        target_stack: List[str]
        if path in self.prototype.states:
            target_stack = accum
        else:
            # si no, tratar path como un nodo simple (ej: "EstadoVida.Vigilar") y entrar tal cual
            target_stack = [path]

        # hallar prefijo común con la pila actual
        cur = self.active_stack[:]
        common = 0
        for a, b in zip(cur, target_stack):
            if a == b:
                common += 1
            else:
                break

        # ejecutar exit actions de los estados que se van a dejar
        for s in reversed(cur[common:]):
            self._call_exit_actions(s)

        # entrar en los estados faltantes
        for s in target_stack[common:]:
            self.active_stack.append(s)
            self._call_entry_actions(s, self.blackboard.get("entity"))
            # si es composite, gestionar initial / history
            try:
                proto = self._get_state_proto(s)
            except KeyError:
                continue
            if proto.stype == "composite":
                # si existe deep history, restaurarla y exponer en blackboard para debug/visual
                if proto.history == "deep" and self.history.get(s):
                    for hist_sub in self.history[s]:
                        self._enter_path(hist_sub)
                    return
                # descender por initial si hay
                elif proto.initial:
                    child_path = f"{s}.{proto.initial}"
                    self._enter_path(child_path)
                    return

    def _exit_to_common_ancestor(self, target_path: str):
        """
        Descripción
            MÉTODO: Sale de los estados activos hasta alcanzar el ancestro común con target_path.
            Comportamiento:
              - Por cada estado que se sale, ejecutar exit actions.
              - Si el padre del estado actual declara history="deep", guardar un snapshot
                de la porción de la pila que pertenece a ese padre en `self.history[parent]`.

        Argumentos
            - target_path (str): ruta destino usada para determinar el ancestro común.

        Retorno
            - None

        Notas de implementación
            - El cálculo del `parent` evita crear nombres inválidos: si el estado actual
              no tiene padre (primer nivel) no se intenta guardar history.
            - Las snapshots se guardan antes de poppear el estado para captar la porción
              activa completa correspondiente al parent.
        """
        target_parts = self._split_path(target_path)
        while self.active_stack:
            cur = self.active_stack[-1]
            cur_parts = self._split_path(cur)
            # si cur es ancestro de target -> detener
            if len(cur_parts) <= len(target_parts) and target_parts[:len(cur_parts)] == cur_parts:
                break
            # si el padre del estado actual declara history="deep" guardamos snapshot
            parent = ".".join(cur_parts[:-1]) if len(cur_parts) > 1 else None
            if parent is not None:
                try:
                    parent_proto = self._get_state_proto(parent)
                    if parent_proto.history == "deep":
                        # guardamos la porción activa que pertenece al parent (antes de pop)
                        parent_prefix = parent + "."
                        self.history[parent] = [s for s in self.active_stack if s.startswith(parent_prefix)]
                except KeyError:
                    # si no existe el prototipo no hacemos nada
                    pass
            # ejecutar exit actions del estado actual
            self._call_exit_actions(cur, self.blackboard.get("entity"))
            self.active_stack.pop()

    # --------------------
    # Ciclo de actualización
    # --------------------
    def update(self, entity: Any, dt: float):
        """
        Descripción
            MÉTODO: Actualización por tick de la HSM. Realiza las tareas necesarias para
            avanzar la máquina de estados en un frame de simulación.

        Argumentos
            - entity (Any): la entidad vinculada a esta HSM (pasada a acciones/condiciones).
            - dt (float): delta-time del frame (segundos).

        Retorno
            - None

        Pasos ejecutados (secuencial):
            1) Escribir `dt` y `entity` en el blackboard.
            2) Ejecutar las acciones de `update` desde la hoja activa hacia la raíz (bottom-up).
            3) Evaluar las transiciones en orden hoja→raíz, exponiendo `cond_params` temporalmente.
            4) Seleccionar la transición de mayor prioridad y, si existe, aplicar:
               - llamar `_exit_to_common_ancestor` con el target,
               - llamar `_enter_path` para posicionar la máquina en el destino.
        """
        self.blackboard["_dt"] = dt
        self.blackboard["entity"] = entity

        # 1) ejecutar update actions hoja->arriba
        for state_path in reversed(self.active_stack):
            try:
                proto = self._get_state_proto(state_path)
            except KeyError:
                continue
            for act in proto.update:
                try:
                    act(self, entity)
                except Exception as err:
                    print(f"[HSM UPDATE] Error en action {act}: {err}")

        # 2) evaluar transiciones: desde la hoja hacia la raíz
        candidates: List[Tuple[int, TransitionPrototype, str]] = []
        for state_path in reversed(self.active_stack):
            try:
                proto = self._get_state_proto(state_path)
            except KeyError:
                continue
            for t in proto.transitions:
                # exponer parámetros de la transición para condiciones
                self.blackboard["_last_transition_cond_params"] = getattr(t, "cond_params", {}) or {}
                if t.cond is None:
                    candidates.append((t.priority, t, state_path))
                else:
                    try:
                        if t.cond(self, entity):
                            candidates.append((t.priority, t, state_path))
                    except Exception as err:
                        print(f"[HSM TRANSITION] Error evaluando condición {t}: {err}")
                        # ignorar condición con error
                        continue
        # limpiar parámetros transitorios
        self.blackboard["_last_transition_cond_params"] = {}

        if not candidates:
            return

        # escoger la transición de mayor prioridad (si empatan, la primera encontrada)
        candidates.sort(key=lambda x: -x[0])
        _, chosen, origin = candidates[0]
        target = chosen.to

        # ejecutar salida hasta ancestro común y entrar en target
        try:
            self._exit_to_common_ancestor(target)
            self._enter_path(target)
        except Exception as err:
            print(f"[HSM] Error al aplicar transición a {target}: {err}")

    # --------------------
    # API pública sencilla
    # --------------------
    def get_active_stack(self) -> List[str]:
        """
        Descripción
            MÉTODO: Devuelve una copia de la pila activa (root -> ... -> hoja).

        Argumentos
            - Ninguno

        Retorno
            - List[str]: copia de `self.active_stack`.
        """
        return list(self.active_stack)

    def set_blackboard(self, key: str, val: Any):
        """
        Descripción
            MÉTODO: Asigna un valor en el blackboard compartido.

        Argumentos
            - key (str): clave a escribir.
            - val (Any): valor asociado a la clave.

        Retorno
            - None
        """
        self.blackboard[key] = val

    def get_blackboard(self, key: str, default: Any = None):
        """
        Descripción
            MÉTODO: Obtiene un valor del blackboard.

        Argumentos
            - key (str): clave a leer.
            - default (Any): valor por defecto si la clave no existe.

        Retorno
            - Any: valor asociado a la clave o `default` si no existe.
        """
        return self.blackboard.get(key, default)