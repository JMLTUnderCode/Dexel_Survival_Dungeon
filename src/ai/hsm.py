"""
HSM runtime core.

Proporciona:
- StatePrototype, TransitionPrototype: estructuras inmutables creadas por el builder.
- HSMInstance: runtime que mantiene la pila activa (deep history support) y ejecuta
  entry/update/exit actions (callables) y evalúa transiciones.

Diseño ligero: acciones y condiciones son callables pasados por el builder.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

Action = Callable[[Any, Any], None]      # (hinst, entity)
Condition = Callable[[Any, Any], bool]   # (hinst, entity)

@dataclass
class TransitionPrototype:
    to: str                              # path string, e.g. "EstadoVida.Atacar" or "EstadoVida"
    cond: Optional[Condition] = None
    priority: int = 100
    cond_params: Dict[str, Any] = field(default_factory=dict)
    restore_history: bool = False

@dataclass
class StatePrototype:
    name: str
    stype: str = "leaf"                  # "leaf" | "composite"
    entry: List[Action] = field(default_factory=list)
    update: List[Action] = field(default_factory=list)
    exit: List[Action] = field(default_factory=list)
    substates: List[str] = field(default_factory=list)
    initial: Optional[str] = None
    transitions: List[TransitionPrototype] = field(default_factory=list)
    history: Optional[str] = None        # "deep" | "shallow" | None

@dataclass
class HSMPrototype:
    name: str
    params: Dict[str, Any]
    states: Dict[str, StatePrototype]
    root: str = "root"

class StateInstance:
    def __init__(self, proto: StatePrototype, path: str):
        self.proto = proto
        self.path = path     # full path e.g. "EstadoVida.Atacar"
        self.children: List[StateInstance] = []

class HSMInstance:
    """
    Runtime HSM instance.
    - prototype: HSMPrototype
    - blackboard: dict (contains _dt, _spec_params)
    - active_stack: list of state path strings from root -> leaf
    - history: mapping state_path -> saved active stack fragment (for deep history)
    """
    def __init__(self, prototype: HSMPrototype, blackboard: Optional[Dict[str,Any]] = None):
        self.prototype = prototype
        self.blackboard: Dict[str,Any] = {} if blackboard is None else dict(blackboard)
        self.blackboard.setdefault("_spec_params", prototype.params)
        self.active_stack: List[str] = []
        self.history: Dict[str, List[str]] = {}   # deep history: state_path -> stack fragment
        # initialize root
        self._enter_path(self.prototype.root)

    # internal helpers
    def _enter_initial(self):
        root = self.proto.root_path
        self._enter_state_by_path(root)

    def _get_state_proto(self, path: str) -> StatePrototype:
        # try exact key first
        if path in self.prototype.states:
            return self.prototype.states[path]
        # fallback 1: try last segment (e.g. "root.EstadoVida" -> "EstadoVida")
        last = path.split(".")[-1]
        if last in self.prototype.states:
            return self.prototype.states[last]
        # fallback 2: if path starts with root prefix, try stripping it
        root_prefix = f"{self.prototype.root}."
        if path.startswith(root_prefix):
            alt = path[len(root_prefix):]
            if alt in self.prototype.states:
                return self.prototype.states[alt]
        # not found -> raise original KeyError
        raise KeyError(path)

    def _split_path(self, path: str) -> List[str]:
        return path.split(".")

    def _enter_state_by_path(self, path: str):
        # enter path components from nearest existing prefix
        # find deepest common prefix with current stack to avoid double-exit/enter
        cur = self.active_stack[:]
        # compute target full stack
        target_stack = []
        parts = path.split(".")
        acc = []
        for p in parts:
            acc.append(p if not acc else f"{acc[-1]}.{p}" )
        # if path might be absolute stored as full path already use it
        if path in self.proto.states:
            # build ancestors list
            anc = []
            comp = path.split(".")
            for i in range(len(comp)):
                anc_path = ".".join(comp[:i+1])
                anc.append(anc_path)
            target_stack = anc
        else:
            # fallback: treat path as direct key if present
            target_stack = [path]

        # find common prefix length
        common = 0
        for a, b in zip(cur, target_stack):
            if a == b:
                common += 1
            else:
                break
        # exit from current top down to common+1
        for s in reversed(cur[common:]):
            self._call_exit_actions(s)
        # enter missing states from common -> end
        for s in target_stack[common:]:
            self.active_stack.append(s)
            self._call_entry_actions(s)
            # if composite with initial and not yet at leaf, descend to its initial
            sp = self.proto.states.get(s)
            if sp and sp.type == "composite":
                init = sp.initial or (sp.substates[0] if sp.substates else None)
                if init:
                    # construct child full path
                    child_path = f"{s}.{init}"
                    self._enter_state_by_path(child_path)
                    # after recursive entry, stop (entry recursive handled)
                    return

    def _call_entry_actions(self, state_path: str, entity: Any = None):
        sp = self.proto.states.get(state_path)
        if not sp:
            return
        for act in sp.entry:
            try:
                act(self, entity)
            except Exception:
                continue

    def _call_update_actions(self, state_path: str, entity: Any = None):
        sp = self.proto.states.get(state_path)
        if not sp:
            return
        for act in sp.update:
            try:
                act(self, entity)
            except Exception:
                continue

    def _call_exit_actions(self, state_path: str, entity: Any = None):
        sp = self.proto.states.get(state_path)
        if not sp:
            return
        for act in sp.exit:
            try:
                act(self, entity)
            except Exception:
                continue

    def _current_leaf(self) -> Optional[str]:
        return self.active_stack[-1] if self.active_stack else None


    def _enter_path(self, path: str):
        """
        Enter a state path from its parent context. Will push initial substates as needed.
        """
        parts = self._split_path(path)
        accum = []
        for i, part in enumerate(parts):
            accum.append(part if i==0 else f"{accum[-1]}.{part}")
            p = accum[-1]
            if p in self.active_stack:
                continue
            proto = self._get_state_proto(p)
            # run entry actions
            for a in proto.entry:
                try:
                    a(self, self.blackboard.get("entity"))
                except Exception:
                    pass
            self.active_stack.append(p)
            # descend into initial if composite
            if proto.stype == "composite":
                # decide initial: history or explicit initial
                if proto.history == "deep" and self.history.get(p):
                    # restore deep history
                    for sub in self.history[p]:
                        self._enter_path(sub)
                    return
                initial = proto.initial
                if initial:
                    child_path = f"{p}.{initial}"
                    self._enter_path(child_path)
                    return

    def _exit_to_common_ancestor(self, target_path: str):
        """
        Exit active states until reaching common ancestor with target_path.
        Save deep history as required.
        """
        # find common prefix
        target_parts = self._split_path(target_path)
        while self.active_stack:
            cur = self.active_stack[-1]
            cur_parts = self._split_path(cur)
            # if cur is ancestor of target -> stop
            if len(cur_parts) <= len(target_parts) and target_parts[:len(cur_parts)] == cur_parts:
                break
            # else exit cur
            proto = self._get_state_proto(cur)
            # save deep history if parent has history="deep"
            parent = ".".join(cur_parts[:-1]) if len(cur_parts) > 1 else cur_parts[0]
            if parent in self.prototype.states:
                parent_proto = self._get_state_proto(parent)
                if parent_proto.history == "deep":
                    # store copy of active stack fragment under parent
                    self.history[parent] = list(filter(lambda s: s.startswith(parent + "."), self.active_stack))
            # run exit actions
            for a in reversed(proto.exit):
                try:
                    a(self, self.blackboard.get("entity"))
                except Exception:
                    pass
            self.active_stack.pop()

    def _reconstruct_path_chain(self, to_path: str) -> List[str]:
        """
        Ensure the full chain to `to_path` exists in prototypes (sanity).
        Returns list of path levels to enter (from shallow to deep).
        """
        return self._split_path(to_path)
    
    def update(self, entity: Any, dt: float):
        """
        One tick update: set _dt, run updates from deepest active state upward,
        and evaluate transitions (deepest first).
        """
        self.blackboard["_dt"] = dt
        self.blackboard["entity"] = entity
        # 1) run update actions from deepest to shallowest
        for state_path in reversed(self.active_stack):
            proto = self._get_state_proto(state_path)
            for u in proto.update:
                try:
                    u(self, entity)
                except Exception:
                    pass
        # 2) evaluate transitions: deepest first; respect priority
        # collect transitions along active stack
        transitions_candidates: List[Tuple[int, TransitionPrototype, str]] = []
        for state_path in reversed(self.active_stack):
            proto = self._get_state_proto(state_path)
            for t in proto.transitions:
                # ensure transition cond params are available to condition functions
                self.blackboard["_last_transition_cond_params"] = getattr(t, "cond_params", {}) or {}
                if t.cond is None:
                    transitions_candidates.append((t.priority, t, state_path))
                else:
                    try:
                        if t.cond(self, entity):
                            transitions_candidates.append((t.priority, t, state_path))
                    except Exception:
                        # if condition raises, ignore this transition
                        pass
        # clear last_transition_cond_params after evaluation
        self.blackboard["_last_transition_cond_params"] = {}
        if not transitions_candidates:
            return
        # pick highest priority
        transitions_candidates.sort(key=lambda x: -x[0])
        _, chosen_t, origin = transitions_candidates[0]
        # perform transition to chosen_t.to (string)
        target = chosen_t.to
        # exit until common ancestor
        self._exit_to_common_ancestor(target)
        # enter target path
        self._enter_path(target)

    def _execute_transition(self, from_state: str, transition: TransitionPrototype, entity: Any):
        # save history for composite ancestors if needed
        # find common ancestor path for from_state and to_state
        to_path = transition.to_path
        # exit from current leaf up to the ancestor where diverge
        target_parts = to_path.split(".")
        # normalize target full path: try to expand if target refers to nested child without full path
        if to_path not in self.proto.states:
            # attempt to resolve relative path (simple case)
            pass
        # compute stacks
        cur = self.active_stack[:]
        # compute target_stack similarly to enter helper
        target_stack = []
        comp = to_path.split(".")
        for i in range(len(comp)):
            anc_path = ".".join(comp[:i+1])
            target_stack.append(anc_path)
        # find common prefix
        common = 0
        for a, b in zip(cur, target_stack):
            if a == b:
                common += 1
            else:
                break
        # before exiting, if any composite in cur[common-1] has history enabled, save snapshot
        for idx in range(common, len(cur)):
            parent = ".".join(cur[idx].split(".")[:-1])
            # save deep history for any ancestor that declares history
            # we'll store snapshots at composite paths
        # exit states from top down to common
        for s in reversed(cur[common:]):
            self._call_exit_actions(s, entity)
            self.active_stack.pop()
        # if transition requests restore_history and target is composite with history, attempt to restore
        if transition.restore_history:
            # apply deep history restore for target composite if exists
            # if history snapshot exists, push it; otherwise enter initial
            hist = self.history.get(target_stack[0])
            if hist:
                for s in hist:
                    self.active_stack.append(s)
                    self._call_entry_actions(s, entity)
                return
        # otherwise enter target stack missing parts
        for s in target_stack[common:]:
            self.active_stack.append(s)
            self._call_entry_actions(s, entity)
            sp = self.proto.states.get(s)
            if sp and sp.type == "composite":
                init = sp.initial or (sp.substates[0] if sp.substates else None)
                if init:
                    child_path = f"{s}.{init}"
                    self._enter_state_by_path(child_path)
                    return

    # helpers for external use
    def get_active_stack(self) -> List[str]:
        return list(self.active_stack)

    def set_blackboard(self, key: str, val: Any):
        self.blackboard[key] = val

    def get_blackboard(self, key: str, default: Any = None):
        return self.blackboard.get(key, default)