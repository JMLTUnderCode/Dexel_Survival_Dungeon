"""
Componente Behavior — documentación general

Propósito
---------
Este módulo expone la clase `Behavior` que actúa como envoltorio (wrapper)
runtime para ejecutar una HSM (Hierarchical State Machine) asociada a una entidad
(enemigo). `Behavior` encapsula la instancia de la HSM (`HSMInstance`) y
proporciona una API simple para integrarla en el ciclo de vida del enemigo.

Resumen funcional
-----------------
- Construcción: `Behavior.from_spec(spec, entity, manager)` construye el prototype
  mediante `build_from_spec` y crea la instancia runtime `HSMInstance`.
- Ejecución: `Behavior.tick(dt)` delega la actualización por frame a la HSM.
- Consulta: `Behavior.get_active_stack()` devuelve la pila de estados activa.
- Inicio/Parada: `start()` y `stop()` permiten hooks para inicialización/limpieza.

Puntos clave de diseño
----------------------
1. Separación de responsabilidades:
   - El builder ([`build_from_spec`](src/ai/hsm_builder.py)) convierte la spec declarativa
     en un prototype (HSMPrototype). Ver: src/ai/hsm_builder.py.
   - El runtime (`HSMInstance`) ejecuta la lógica de entrada/salida e historial.
     Ver: [`HSMInstance`](src/ai/hsm.py).
   - `Behavior` solo orquesta la creación y la exposición simple de la HSM para la entidad.

2. Blackboard:
   - `Behavior` inyecta referencias esenciales en el blackboard (manager, entity,
     `_spec_params`, `path_offset`) para que acciones/condiciones puedan consultarlas.
   - Convención de claves: `_spec_params`, `manager`, `entity_manager`, `entity`, `path_offset`.

3. Buenas prácticas:
   - Mantener las acciones y condiciones en sus módulos (`src/ai/actions.py`, `src/ai/conditions.py`).
   - Evitar lógica de juego dentro de `Behavior`; delegar en acciones/condiciones.

Ejemplo mínimo de uso
---------------------
1) Definir spec (p. ej. `GUARDIAN_BEHAVIOR` en `src/data/enemies.py`).
2) Crear enemy y manager (EntityManager).
3) Adjuntar behavior:
   behavior = Behavior.from_spec(spec, enemy, entity_manager)
   enemy.behavior = behavior
4) En el update del enemigo llamar:
   behavior.tick(dt)

Referencias en el workspace
---------------------------
- Builder: [`build_from_spec`](src/ai/hsm_builder.py)
- Runtime: [`HSMInstance`](src/ai/hsm.py)
- Actions registry: src/ai/actions.py
- Conditions registry: src/ai/conditions.py
- Spec ejemplo: src/data/enemies.py
"""

from __future__ import annotations
from typing import Any, Dict

from ai.hsm_builder import build_from_spec
from ai.hsm import HSMInstance, HSMPrototype

class Behavior:
    """
    Descripción
        CLASE: Wrapper runtime que asocia una instancia de HSM con una entidad (enemy).

    Atributos
        - hinst (HSMInstance): Instancia runtime de la HSM.
        - spec (Dict[str, Any]): Spec declarativa usada para construir la HSM.
        - entity (Any): Entidad a la que se asocia este Behavior (usualmente Enemy).
        - manager (Any): Manager (EntityManager) usado por acciones/condiciones.

    Métodos y Funciones
        - from_spec: Construye Behavior desde spec y lo adjunta a la entidad.
        - tick: Ejecuta un paso (update) de la HSM.
        - get_active_stack: Devuelve la pila de estados actual para debugging.
        - start / stop: Hooks opcionales de inicio/parada.
    """

    def __init__(self, hinst: HSMInstance, spec: Dict[str, Any], entity: Any, manager: Any):
        """
        Descripción
            MÉTODO: Inicializador de Behavior que registra referencias esenciales en el blackboard.

        Argumentos
            - hinst (HSMInstance) : Instancia runtime de la HSM.
            - spec (Dict[str, Any]) : Spec declarativa original.
            - entity (Any) : Entidad (Enemy) asociada.
            - manager (Any) : EntityManager o servicio equivalente.
        """
        # 1. Almacenar referencias
        self.hinst = hinst
        self.spec = spec
        self.entity = entity
        self.manager = manager

        # 2. Inyectar referencias útiles en el blackboard para acciones y condiciones
        #    - entity_manager: acceso a pathfinder, player, etc.
        #    - entity: referencia a la entidad concreta
        #    - _spec_params: parámetros del spec para condiciones
        #    - path_offset: valor conveniente expuesto desde la entidad
        try:
            self.hinst.set_blackboard("entity_manager", manager)
            self.hinst.set_blackboard("entity", entity)
            self.hinst.set_blackboard("_spec_params", spec.get("params", {}))
        except Exception as e:
            print(f"[BEHAVIOR INIT] Error setting blackboard values: {e}")
            # No queremos romper la creación de Behavior si el blackboard falla
            pass

    @classmethod
    def from_spec(cls, spec: Dict[str, Any], entity: Any, manager: Any) -> "Behavior":
        """
        Descripción
            FUNCIÓN: Construye un Behavior desde una spec declarativa (dict).

        Argumentos
            - spec (Dict[str, Any]) : Especificación declarativa de la HSM (p. ej. GUARDIAN_BEHAVIOR).
            - entity (Any) : Entidad (Enemy) que recibirá el comportamiento.
            - manager (Any) : EntityManager que provee servicios (player, pathfinder).

        Retorno
            - Behavior: instancia lista para ser usada por la entidad.
        """
        if not isinstance(spec, dict):
            raise TypeError("Behavior.from_spec: expected spec dict")

        # 1) Convertir la spec a un prototype usando el builder
        proto: HSMPrototype = build_from_spec(spec)

        # 2) Crear blackboard inicial con referencias y parámetros del spec
        initial_bb: Dict[str, Any] = {
            "_spec_params": spec.get("params", {}),
            "manager": manager,
            "entity_manager": manager,
            "entity": entity,
            "path_offset": getattr(entity, "path_offset", 1.0),
        }

        # 3) Instanciar el runtime HSM
        hinst = HSMInstance(proto, blackboard=initial_bb)

        # 4) Devolver Behavior construido
        return cls(hinst=hinst, spec=spec, entity=entity, manager=manager)

    def tick(self, dt: float) -> None:
        """
        Descripción
            MÉTODO: Ejecuta un paso de la HSM (llamado cada frame por Enemy.update).

        Argumentos
            - dt (float) : tiempo en segundos transcurrido desde el último frame.
        """
        try:
            # Registrar dt y delegar la actualización a la HSMInstance
            self.hinst.update(self.entity, dt)
        except Exception as e:
            print(f"[BEHAVIOR] Error during tick: {e}")
            # No queremos que un fallo en la HSM detenga el juego
            pass

    def get_active_stack(self) -> list[str]:
        """
        Descripción
            FUNCIÓN: Devuelve una copia de la pila de estados activos de la HSM.

        Retorno
            - list[str]: lista de rutas desde 'root' hasta la hoja activa.
        """
        try:
            return self.hinst.get_active_stack()
        except Exception:
            return []

    def start(self) -> None:
        """
        Descripción
            MÉTODO: Hook opcional invocado tras crear el Behavior. Aquí se pueden
            ejecutar inicializaciones adicionales si fueran necesarias.
        """
        return

    def stop(self) -> None:
        """
        Descripción
            MÉTODO: Limpia referencias en el blackboard para evitar fugas
            cuando el Behavior deja de usarse.
        """
        try:
            self.hinst.set_blackboard("entity", None)
            self.hinst.set_blackboard("manager", None)
            self.hinst.set_blackboard("entity_manager", None)
        except Exception as e:
            print(f"[BEHAVIOR STOP] Error setting blackboard values: {e}")
            pass