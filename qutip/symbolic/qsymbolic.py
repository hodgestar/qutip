"""
Core of the symbolic quantum object representation.
"""

from __future__ import annotations

import typing

from .nodes import to_node, sum


if typing.TYPE_CHECKING:
    from qutip import Qobj
    from qutip.typing import LayerType
    from .nodes import SymbolicNode


class Qsymbolic:
    """
    The symbolic equivalent of Qobj and QobjEvo.
    """

    def __init__(self, node: SymbolicNode | None = None):
        self._node = node

    @property
    def dims(self) -> list[list[int]] | list[list[list[int]]]:
        return self._node.dims.as_list()

    @property
    def type(self) -> str:
        return self._node.dims.type

    @property
    def superrep(self) -> str:
        return self._node.dims.superrep

    @property
    def data(self) -> None:
        # TODO: Extend the error message to explain how to obtain data.
        #       E.g. by converting the QSymbolic to Qobj first.
        raise TypeError("QSymbolic does not support direct conversion to data.")

    @property
    def dtype(self) -> None:
        raise TypeError("QSymbolic does not have a dtype.")

    def to(self, data_type: LayerType, copy: bool = False) -> Qobj:
        raise TypeError("QSymbolic does not have a dtype to alter.")

    def __add__(self, other: Qobj | Qsymbolic | complex | float | int) -> Qsymbolic:
        if other == 0:
            return self
        other = to_node(other)
        return sum.from_terms((self, other))

    def __radd__(self, other: Qobj | Qsymbolic | complex | float | int) -> Qsymbolic:
        if other == 0:
            return self
        other = to_node(other)
        return sum.from_terms((other, self))

    def __sub__(self, other: Qobj | Qsymbolic | complex | float | int) -> Qsymbolic:
        if other == 0:
            return self
        other = to_node(other)
        # TODO: Implement
        XXX

    def __rsub__(self, other: Qobj | Qsymbolic | complex | float | int) -> Qsymbolic:
        # TODO: Implement
        # return self.__neg__().__add__(other)
        XXX
