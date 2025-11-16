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

Patrones y buenas prácticas
---------------------------
- Acciones/condiciones:
  - Firma: fn(hinst, entity). Usar el blackboard para compartir datos y params.
  - No hacer operaciones pesadas en condiciones; cachear en blackboard si es necesario.
- Restore history:
  - Usar `restore_history=True` en la transición Curarse->EstadoVida para que la
    HSM restaure la subruta previa (deep history) y deje que el subestado restaurado
    evalúe sus propias transiciones (p.ej. Atacar -> RegresarAZona).
- Blackboard keys recomendadas:
  - `_spec_params`: parámetros del spec.
  - `manager`, `entity_manager`: accesos a servicios (pathfinder, player).
  - `return_target_pos`, `is_returning_to_zone`, `is_at_protection_zone`: convenciones para acciones de retorno.

Ejemplo de flujo (guardian)
---------------------------
1. root -> EstadoVida (composite) -> EstadoVida.Vigilar (leaf).
2. Si `PlayerVisible` en Vigilar -> transición a EstadoVida.Atacar.
3. Si en Atacar `IsFarFromProtectionZone` -> transición a EstadoVida.RegresarAZona.
4. En RegresarAZona la acción `return_to_protection_zone` crea `entity.temp_follow_path`
   y asigna `entity.algorithm = "TEMP_PATH_FOLLOWING"`. `check_return_path_finished`
   marca `is_at_protection_zone` al llegar.
5. Si en cualquier leaf `HealthBelow` -> transición a Huyendo (nivel 1).
6. Curarse emplea `restore_history=True` para volver a EstadoVida y reanudar el subestado previo.

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
    Representación de una transición en el prototipo de HSM.

    Atributos:
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
    Prototipo de estado.

    Campos:
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
    Contenedor del spec construido por el builder.
    """
    name: str
    params: Dict[str, Any]
    states: Dict[str, StatePrototype]
    root: str = "root"


class HSMInstance:
    """
    Instancia en ejecución de la HSM.

    Responsabilidades:
      - Mantener prototype (HSMPrototype).
      - Mantener blackboard (datos compartidos).
      - Mantener active_stack: rutas activas desde root hasta la hoja.
      - Mantener history para deep history de composites.

    Nota:
      - Todas las acciones/condiciones se ejecutan con la firma (hinst, entity).
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
        Resuelve una ruta a un StatePrototype con varias heurísticas:
          - clave exacta en prototype.states
          - último segmento (p. ej. "root.X" -> "X")
          - si inicia con "root." intentar la parte sin prefijo
        Lanza KeyError si no encuentra el prototipo.
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
        return path.split(".")

    # --------------------
    # Ejecución de acciones
    # --------------------
    def _call_actions(self, actions: List[Action], entity: Any, kind: str):
        for act in actions:
            try:
                act(self, entity)
            except Exception as err:
                print(f"[HSM {kind}] Error en acción {act}: {err}")

    def _call_entry_actions(self, state_path: str, entity: Any = None):
        try:
            proto = self._get_state_proto(state_path)
        except KeyError:
            return
        self._call_actions(proto.entry, entity, "ENTRY")

    def _call_update_actions(self, state_path: str, entity: Any = None):
        try:
            proto = self._get_state_proto(state_path)
        except KeyError:
            return
        self._call_actions(proto.update, entity, "UPDATE")

    def _call_exit_actions(self, state_path: str, entity: Any = None):
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
        Entra en la ruta 'path' (puede ser fully-qualified o relativa).
        Realiza:
          - calcular la secuencia de nodos a introducir en la pila
          - ejecutar entry actions y descender por initial si el estado es composite
          - restaurar history deep cuando corresponda
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
                # restaurar deep history si existe
                if proto.history == "deep" and self.history.get(s):
                    # insertar la secuencia histórica
                    for hist_sub in self.history[s]:
                        self._enter_path(hist_sub)
                    return
                # descender por initial si hay
                if proto.initial:
                    child_path = f"{s}.{proto.initial}"
                    self._enter_path(child_path)
                    return

    def _exit_to_common_ancestor(self, target_path: str):
        """
        Sale de los estados activos hasta alcanzar el ancestro común con target_path.
        Guarda snapshots de deep history cuando corresponde.
        Ejecuta exit actions durante el proceso.
        """
        target_parts = self._split_path(target_path)
        while self.active_stack:
            cur = self.active_stack[-1]
            cur_parts = self._split_path(cur)
            # si cur es ancestro de target -> detener
            if len(cur_parts) <= len(target_parts) and target_parts[:len(cur_parts)] == cur_parts:
                break
            # si el padre del estado actual declara history="deep" guardamos snapshot
            try:
                proto = self._get_state_proto(cur)
            except KeyError:
                self.active_stack.pop()
                continue
            parent = ".".join(cur_parts[:-1]) if len(cur_parts) > 1 else cur_parts[0]
            if parent in self.prototype.states:
                try:
                    parent_proto = self._get_state_proto(parent)
                    if parent_proto.history == "deep":
                        # guardamos la porción activa que pertenece al parent
                        self.history[parent] = [s for s in self.active_stack if s.startswith(parent + ".")]
                except KeyError:
                    pass
            # ejecutar exit actions del estado actual
            self._call_exit_actions(cur, self.blackboard.get("entity"))
            self.active_stack.pop()

    # --------------------
    # Ciclo de actualización
    # --------------------
    def update(self, entity: Any, dt: float):
        """
        Actualización por tick:
          - registra dt y entity en blackboard
          - ejecuta update actions desde la hoja hacia arriba
          - evalúa transiciones (hoja -> raíz) y aplica la de mayor prioridad
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
        """Devuelve la pila activa (copia)."""
        return list(self.active_stack)

    def set_blackboard(self, key: str, val: Any):
        """Asigna un valor en el blackboard."""
        self.blackboard[key] = val

    def get_blackboard(self, key: str, default: Any = None):
        """Obtiene un valor del blackboard."""
        return self.blackboard.get(key, default)