"""
Utilidades compartidas para acciones/condiciones HSM.

Contiene helpers ligeros y sin efectos secundarios que resuelven parámetros
del spec, obtienen referencias comunes (manager/player) desde el blackboard
y manejo de excepciones.

Objetivo:
- Evitar duplicación de código entre `src/ai/actions.py` y `src/ai/conditions.py`.
- Mantener condiciones/actions limpias y enfocadas en su responsabilidad.
"""
from typing import Any, Optional
from ai.hsm import HSMInstance

def get_spec_param(hinst: HSMInstance, key: Optional[str], default: Any = None) -> Any:
    """
    Descripción
        FUNCIÓN: Resuelve un parámetro que puede ser:
            - un número (int/float) -> devuelto tal cual,
            - una clave string que existe en `_spec_params` del blackboard -> su valor,
            - un literal numérico en forma de string -> convertido a float,
            - None -> default.
    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard.
        - key (Optional[str]): clave o literal a resolver.
        - default (Any): valor por defecto si no se resuelve.
    Retorno
        - Any: valor resuelto o default.
    """
    spec = hinst.blackboard.get("_spec_params", {})
    if key is None:
        return default
    if isinstance(key, (int, float)):
        return key
    if isinstance(key, str):
        if key in spec:
            return spec[key]
        try:
            return float(key)
        except Exception:
            return default
    return default

def get_manager(hinst: HSMInstance) -> Optional[Any]:
    """
    Obtiene manager de forma segura desde el blackboard.
    - manager: hinst.blackboard['manager'] o None
    """
    return hinst.blackboard.get("manager")

def get_player(hinst: HSMInstance) -> Optional[Any]:
    """
    Obtiene player de forma segura desde el blackboard.
    - player: getattr(manager, 'player', None) o None
    """
    manager = hinst.blackboard.get("manager")
    player = getattr(manager, "player", None) if manager else None
    return player

def exception_print(tag: str, entity: Any, err: str):
    """Wrapper ligero para mensajes de debug (se puede reemplazar por logger)."""
    print(f"[{tag}] Entity: {entity}. \n\n {err}")
