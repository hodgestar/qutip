"""
Core for writing functions to process trees of symbolic nodes.
"""

from __future__ import annotations

import functools
from typing import Callable

from ..nodes import SymbolicNode
from ..qsymbolic import Qsymbolic


def stypedispatch(func):
    """
    Single-dispatch on `SymbolicNode.stype` generic function decorator.

    Transforms the given function into a generic function, which can
    have different behaviours based on the `stype` of the first argument.

    The decorated function acts as the default implementation. Additional
    implementations may be registered with the `register(stype)`
    decorator of the generic function.

    Implementation functions are always passed a `SymbolicNode` as the
    first argument, but the generic function accepts either `Qsymbolic`
    or `SymbolicNode`.

    Implementation functions may accept additional arguments. All
    implementation functions should accept the same arguments.

    The generic function has the methods `from_symbolic(...)`, which
    accepts only `Qsymbolic` instances as the first argument,
    and `from_node(...)` which accepts only `SymbolicNode`.
    """
    return StypeDispatcher(func)


class StypeDispatcher:
    def __init__(self, func):
        self._default = func
        self._implementations = {}

    def __call__(self, qsym_or_node: Qsymbolic | SymbolicNode, *args, **kw):
        """Call the generic function, dispatching on either `Qsymbolic` or `SymbolicNode` instances.

        Parameters
        ----------
        qsym_or_node:
            The object to dispatch on. If the object is an instance of `Qsymbolic`, and has
            no node, dispatching is skipped and `None` is returned.
        *args, **kw:
            Additional arguments to pass to the implementation functions.
        """
        if isinstance(qsym_or_node, Qsymbolic):
            return self.from_symbolic(qsym_or_node, *args, **kw)
        return self.from_node(qsym_or_node, *args, **kw)

    def from_symbolic(self, qsym: Qsymbolic, *args, **kw):
        """Call the generic function, dispatching only on `Qsymbolic` instances.

        Parameters
        ----------
        qsym:
            The object to dispatch on. If the `Qsymbolic` has no node, dispatching
            is skipped and `None` is returned.
        *args, **kw:
            Additional arguments to pass to the implementation functions.
        """
        if qsym._node is None:
            return None
        return self.from_node(qsym._node, *args, **kw)

    def from_node(self, node: SymbolicNode, *args, **kw):
        """Call the generic function, dispatching only on `SymbolicNode` instances.

        Parameters
        ----------
        node:
            The object to dispatch on.
        *args, **kw:
            Additional arguments to pass to the implementation functions.
        """
        func = self._implementations.get(node.stype, self._default)
        return func(node, *args, *kw)

    def register(self, stype: str, func: Callable | None = None):
        """Register an implementation for a given stype.

        Parameters
        ----------
        stype:
            The symbolic type to register an implementation for.
        func:
            The implementing function. It must accept a `SymbolicNode`
            of the given stype as its first argument.

        If an implementation for `stype` already exists, it is replaced.
        """
        if func is None:
            return functools.partial(self.register, stype)
        self._implementations[stype] = func
        return func
