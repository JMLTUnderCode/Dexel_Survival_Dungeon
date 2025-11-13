"""
Behavior component: wrapper runtime que asocia HSMInstance con la entidad.

API:
- Behavior.from_spec(spec, entity, manager) -> Behavior
- behavior.tick(dt)
- behavior.get_active_state_stack() -> list[str]
"""
from __future__ import annotations
from typing import Any, Dict, Optional

from ai.hsm_builder import build_from_spec
from ai.hsm import HSMInstance, HSMPrototype

class Behavior:
    """
    Comportamiento delegado para una entidad.
    - from_spec(spec, entity, manager): crea instancia runtime desde spec declarativa (dict).
    - tick(dt): actualiza la HSM runtime.
    - get_active_stack(): devuelve la pila de estados activos para debug.
    """
    def __init__(self, hinst: HSMInstance, spec: Dict[str, Any], entity: Any, manager: Any):
        self.hinst = hinst
        self.spec = spec
        self.entity = entity
        self.manager = manager
        # ensure manager and entity references in blackboard for conditions/actions
        self.hinst.set_blackboard("manager", manager)
        self.hinst.set_blackboard("entity_manager", manager)
        self.hinst.set_blackboard("entity", entity)
        # expose convenient params
        self.hinst.set_blackboard("path_offset", getattr(entity, "path_offset", 1.0))

    @classmethod
    def from_spec(cls, spec: Dict[str, Any], entity: Any, manager: Any) -> "Behavior":
        """
        Construye Behavior desde spec declarativa (dict) y la adjunta a `entity`.
        - spec: dict obtenido (por ejemplo `HUNTER_BEHAVIOR` en src/data/enemies.py`)
        - entity: instancia de Enemy
        - manager: EntityManager (necesario para queries y pathfinder)
        """
        if not isinstance(spec, dict):
            raise TypeError("Behavior.from_spec: expected spec dict")
        proto = build_from_spec(spec)
        # provide initial blackboard containing manager and any spec params
        initial_bb = {
            "_spec_params": spec.get("params", {}),
            "manager": manager,
            "entity_manager": manager,
            "entity": entity,
            "path_offset": getattr(entity, "path_offset", 1.0),
        }
        hinst = HSMInstance(proto, blackboard=initial_bb)
        return cls(hinst=hinst, spec=spec, entity=entity, manager=manager)

    def tick(self, dt: float) -> None:
        """
        Ejecutar un paso de la HSM (llamado por Enemy.update cada frame).
        """
        try:
            self.hinst.update(self.entity, dt)
        except Exception:
            # no elevar excepciones al bucle principal
            pass

    def get_active_stack(self) -> list[str]:
        return self.hinst.get_active_stack()

    def start(self) -> None:
        # placeholder: se llamó al crear la instancia; aquí se podrían ejecutar hooks adicionales
        return

    def stop(self) -> None:
        # limpiar referencias si es necesario
        try:
            self.hinst.set_blackboard("entity", None)
            self.hinst.set_blackboard("manager", None)
        except Exception:
            pass