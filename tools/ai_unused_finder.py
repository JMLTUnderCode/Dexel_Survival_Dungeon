"""
Script ligero para detectar acciones/condiciones NO USADAS por specs HSM.

Uso:
  python3 tools/ai_unused_finder.py

Qué hace:
- importa los registries runtime: ACTIONS (src/ai/actions.py) y CONDITIONS (src/ai/conditions.py)
- importa todos los módulos en src/data/ y busca dicts `*_BEHAVIOR` o variables `...` con claves 'states'
- extrae strings usados en entry/update/exit y transitions.cond
- reporta acciones/condiciones no referenciadas por ninguna spec

NOTA: no modifica código; solo informa. Requiere ejecutar desde el root del repo.
"""
import sys
import os
import importlib
from typing import Set, Any, Tuple

# add 'src' to path so modules import as e.g. data.enemies, ai.actions
SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "src")
sys.path.insert(0, os.path.abspath(SRC_DIR))

# import registries
try:
    import ai.actions as actions_mod
    import ai.conditions as conditions_mod
except Exception as e:
    print("Error importing ai.actions / ai.conditions:", e)
    sys.exit(1)

def collect_strings_from_spec(obj: Any, out_actions: Set[str], out_conds: Set[str]):
    """
    Recorre recursivamente estructuras (dict/list/tuple/str) buscando claves:
      - entry/update/exit -> acciones (strings)
      - transitions -> cond (string) y cond_params (ignored)
    """
    if isinstance(obj, dict):
        # if this dict looks like a state def or spec section
        for k, v in obj.items():
            if k in ("entry", "update", "exit") and isinstance(v, (list, tuple)):
                for item in v:
                    if isinstance(item, str):
                        out_actions.add(item)
            if k == "transitions" and isinstance(v, (list, tuple)):
                for t in v:
                    if isinstance(t, dict):
                        c = t.get("cond")
                        if isinstance(c, str):
                            out_conds.add(c)
                        # also consider action-like keys inside transition? (none by default)
            else:
                collect_strings_from_spec(v, out_actions, out_conds)
    elif isinstance(obj, (list, tuple, set)):
        for it in obj:
            collect_strings_from_spec(it, out_actions, out_conds)
    # strings alone not considered top-level unless part of lists/dicts

def scan_data_modules() -> Tuple[Set[str], Set[str], Set[str]]:
    used_actions = set()
    used_conds = set()
    scanned_modules = set()
    data_pkg = os.path.join(os.path.abspath(SRC_DIR), "data")
    if not os.path.isdir(data_pkg):
        print("No src/data directory found.")
        return used_actions, used_conds, scanned_modules

    for fname in os.listdir(data_pkg):
        if not fname.endswith(".py"):
            continue
        mod_name = f"data.{fname[:-3]}"
        try:
            mod = importlib.import_module(mod_name)
            scanned_modules.add(mod_name)
        except Exception as e:
            # best-effort: skip modules that raise on import
            print(f"Warning: could not import {mod_name}: {e}")
            continue
        # inspect module globals for dict-like specs (states etc)
        for nm, val in vars(mod).items():
            if isinstance(val, dict):
                # heuristic: dict with key "states" is HSM spec
                if "states" in val and isinstance(val["states"], dict):
                    collect_strings_from_spec(val, used_actions, used_conds)
                else:
                    # also scan any nested dicts in the module
                    collect_strings_from_spec(val, used_actions, used_conds)
    return used_actions, used_conds, scanned_modules

def main():
    actions_registry = set(getattr(actions_mod, "ACTIONS", {}).keys())
    conditions_registry = set(getattr(conditions_mod, "CONDITIONS", {}).keys())
    used_actions, used_conds, scanned = scan_data_modules()

    unused_actions = sorted(list(actions_registry - used_actions))
    unused_conditions = sorted(list(conditions_registry - used_conds))

    print("Scanned data modules:", ", ".join(sorted(scanned)))
    print(f"Total registered actions: {len(actions_registry)}  -> used: {len(used_actions)}  unused: {len(unused_actions)}")
    if unused_actions:
        print("\nUnused ACTIONS (candidates to remove):")
        for a in unused_actions:
            print("  -", a)
    else:
        print("\nNo unused ACTIONS detected (based on specs).")

    print(f"\nTotal registered conditions: {len(conditions_registry)}  -> used: {len(used_conds)}  unused: {len(unused_conditions)}")
    if unused_conditions:
        print("\nUnused CONDITIONS (candidates to remove):")
        for c in unused_conditions:
            print("  -", c)
    else:
        print("\nNo unused CONDITIONS detected (based on specs).")

if __name__ == "__main__":
    main()