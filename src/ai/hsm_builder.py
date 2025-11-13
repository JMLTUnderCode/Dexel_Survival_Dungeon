"""
Builder para convertir el spec declarativo (dict) en HSMPrototype.

- Resuelve action keys y condition keys usando registries en src/ai/actions.py
  y src/ai/conditions.py.
- Convierte transiciones, estados y referencias a parámetros (params).
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional
from ai.hsm import HSMPrototype, StatePrototype, TransitionPrototype
import ai.actions as actions_mod
import ai.conditions as conditions_mod

def _resolve_action_list(keys: Optional[List[str]]):
    out = []
    if not keys:
        return out
    for k in keys:
        if isinstance(k, str):
            fn = actions_mod.ACTIONS.get(k)
            if fn:
                out.append(fn)
        elif callable(k):
            out.append(k)
    return out

def _resolve_cond(key: Optional[str]):
    if not key:
        return None
    if isinstance(key, str):
        return conditions_mod.CONDITIONS.get(key)
    if callable(key):
        return key
    return None

def build_from_spec(spec: Dict[str, Any]) -> HSMPrototype:
    """
    Convert a declarative spec (dict) into HSMPrototype.
    """
    states_spec = spec.get("states", {})
    params = spec.get("params", {})

    states: Dict[str, StatePrototype] = {}
    # first pass: create prototypes with empty transitions
    for name, data in states_spec.items():
        stype = data.get("type", "leaf")
        entry = _resolve_action_list(data.get("entry"))
        update = _resolve_action_list(data.get("update"))
        exit = _resolve_action_list(data.get("exit"))
        substates = data.get("substates", [])
        initial = data.get("initial")
        history = data.get("history")
        states[name] = StatePrototype(
            name=name,
            stype=stype,
            entry=entry,
            update=update,
            exit=exit,
            substates=substates,
            initial=initial,
            transitions=[],
            history=history
        )
    # second pass: resolve transitions
    for name, data in states_spec.items():
        trans = []
        for t in data.get("transitions", []):
            cond_key = t.get("cond")
            cond = _resolve_cond(cond_key)
            priority = t.get("priority", 100)
            cond_params = t.get("cond_params", {})
            to = t.get("to")
            restore_history = t.get("restore_history", False)
            trans.append(TransitionPrototype(to=to, cond=cond, priority=priority, cond_params=cond_params, restore_history=restore_history))
        states[name].transitions = trans

    proto = HSMPrototype(
        name=spec.get("name", "unnamed"),
        params=params,
        states=states,
        root=spec.get("root", "root")
    )
    return proto