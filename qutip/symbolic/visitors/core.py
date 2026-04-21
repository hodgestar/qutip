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
    have different behaviours based on the `stype` of the first argument,
    which must be either an instance of `SymbolicNode` or of `Qsymbolic`.

    The decorated function acts as the default implementation. Additional
    implementations may be registered with the `register(stype)`
    decorator of the generic function.
    """
    return StypeDispatcher(func)


class StypeDispatcher:
    def __init__(self, func):
        self._default = func
        self._implementations = {}

    def __call__(self, qsym: Qsymbolic, *args, **kw):
        # TODO: Is None always the right thing to return here?
        if qsym._node is None:
            return None
        return self.from_node(qsym._node)

    def from_symbolic(self, qsym: Qsymbolic, *args, **kw):
        # TODO: Is None always the right thing to return here?
        if qsym._node is None:
            return None
        return self.from_node(qsym._node)

    def from_node(self, node: SymbolicNode, *args, **kw):
        func = self._implementations.get(node.stype, self._default)
        return func(node, *args, *kw)

    def register(self, stype: str, func: Callable | None = None):
        if func is None:
            return functools.partial(self.register, stype)
        self._implementations[stype] = func
        return func
