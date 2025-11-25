"""
Builder para convertir el spec declarativo (dict) en HSMPrototype.

Propósito
---------
Este módulo transforma la especificación declarativa de una HSM (un dict,
p. ej. `GUARDIAN_BEHAVIOR` en src/data/enemies.py a un objeto intermedio 
`HSMPrototype` usado en tiempo de ejecución por `HSMInstance` en src/ai/hsm.py. 
El builder resuelve:
  - las listas de acciones (keys -> callables registradas en `ACTIONS`),
  - las condiciones (keys -> callables registradas en `CONDITIONS`),
  - los parámetros (`params`) y las transiciones (incluyendo `cond_params`
    y `restore_history`).

Qué hace exactamente
---------------------
1. Valida que `spec` sea un diccionario y extrae `states` y `params`.
2. Primera pasada: crea `StatePrototype` por cada estado, resolviendo
   `entry`, `update`, `exit` a listas de callables.
3. Segunda pasada: resuelve las transiciones de cada estado transformando
   las claves de condición en referencias a funciones (o None).
4. Devuelve un `HSMPrototype` listo para que `Behavior.from_spec` cree
   una instancia de runtime (`HSMInstance`).

Formato esperado del spec
-------------------------
spec = {
  "name": "string",
  "params": { ... },
  "root": "root",
  "states": {
    "root": {
      "type": "composite",
      "initial": "SubStateName",      # nombre relativo
      "substates": ["SubStateName", ...],
      "entry": ["action_key", ...],
      "update": [...],
      "exit": [...],
      "transitions": [
         { "to": "TargetState", "cond": "ConditionKey", "priority": 100, "cond_params": {...}, "restore_history": False },
         ...
      ]
    },
    "SomeLeaf": {...}
  }
}

Referencias en el workspace
---------------------------
- Spec ejemplos: src/data/enemies.py
- Builder: this file src/ai/hsm_builder.py
- Actions registry: src/ai/actions.py
- Conditions registry: src/ai/conditions.py
- Runtime prototype types: [`HSMPrototype`](src/ai/hsm.py), [`StatePrototype`](src/ai/hsm.py), [`TransitionPrototype`](src/ai/hsm.py)
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional
from ai.hsm import HSMPrototype, StatePrototype, TransitionPrototype
import ai.actions as actions_mod
import ai.conditions as conditions_mod

def _resolve_action_list(keys: Optional[List[str]]) -> List[callable]:
    """
    Descripción
        FUNCIÓN: Convierte una lista de claves o callables en una lista de
        funciones ejecutables. Soporta:
          - strings: buscados en actions_mod.ACTIONS
          - callables: se usan tal cual

    Argumentos
        - keys (Optional[List[str]]): Lista de claves/callables o None.

    Retorno
        - List[callable]: Lista de funciones resolvidas.
    """
    out = []
    if not keys:
        return out
    for k in keys:
        if isinstance(k, str):
            fn = actions_mod.ACTIONS.get(k)
            if fn:
                out.append(fn)
            else:
                # log ligero para depuración; preferimos continuar en vez de fallar
                print(f"[HSM_BUILDER] Warning: action '{k}' not found in ACTIONS registry.")
        elif callable(k):
            out.append(k)
    return out

def _resolve_cond(key: Optional[str]) -> callable | None:
    """
    Descripción
        FUNCIÓN: Resuelve una clave de condición a la función registrada en
        `conditions_mod.CONDITIONS`. Si la key ya es callable, la devuelve.

    Argumentos
        - key (Optional[str]): nombre de la condición o callable.

    Retorno
        - callable | None
    """
    if not key:
        return None
    if isinstance(key, str):
        cond = conditions_mod.CONDITIONS.get(key)
        if cond is None:
            print(f"[HSM_BUILDER] Warning: condition '{key}' not found in CONDITIONS registry.")
        return cond
    if callable(key):
        return key
    return None

def build_from_spec(spec: Dict[str, Any]) -> HSMPrototype:
    """
    Descripción
        FUNCIÓN: Toma la especificación declarativa de una HSM y la transforma
        en un `HSMPrototype` compuesto por `StatePrototype` y `TransitionPrototype`.

    Argumentos
        - spec (Dict[str, Any]) : Especificación declarativa de la HSM.

    Retorno
        - HSMPrototype: objeto intermedio listo para instanciar `HSMInstance`.
    """
    if not isinstance(spec, dict):
        raise TypeError("build_from_spec: expected spec dict")

    states_spec = spec.get("states", {})
    params = spec.get("params", {})

    if not isinstance(states_spec, dict):
        raise TypeError("build_from_spec: 'states' must be a dict")

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