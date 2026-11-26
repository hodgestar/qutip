"""
Core of the symbolic quantum object representation.
"""

from __future__ import annotations

import typing

from qutip.core.dimensions import Field

from .nodes import adjoint, conjugate, matmul, negate, sum, tensor, to_node, transpose

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
        if isinstance(self._node.dims, Field):
            return "scalar"
        return self._node.dims.type

    @property
    def superrep(self) -> str:
        return self._node.dims.superrep

    @property
    def data(self) -> None:
        raise TypeError(
            "QSymbolic does not support direct conversion to data."
            " Use `qutip.symbolic.visitors.to_qobj(...)` to obtain a"
            " `Qobj` and then access `.data` on it instead."
        )

    @property
    def dtype(self) -> None:
        raise TypeError("QSymbolic does not have a dtype.")

    def to(self, data_type: LayerType, copy: bool = False) -> Qobj:
        raise TypeError("QSymbolic does not have a dtype to alter.")

    def __add__(self, other: Qobj | Qsymbolic | complex) -> Qsymbolic:
        if other == 0:
            return self
        other_node = to_node(other)
        if self._node is None:
            return Qsymbolic(other_node)
        return Qsymbolic(sum.from_terms((self._node, other_node)))

    def __radd__(self, other: Qobj | Qsymbolic | complex) -> Qsymbolic:
        if other == 0:
            return self
        other_node = to_node(other)
        if self._node is None:
            return Qsymbolic(other_node)
        return Qsymbolic(sum.from_terms((other_node, self._node)))

    def __sub__(self, other: Qobj | Qsymbolic | complex) -> Qsymbolic:
        if other == 0:
            return self
        other_node = to_node(other)
        if self._node is None:
            return Qsymbolic(negate.negate(other_node))
        return Qsymbolic(sum.from_terms((self._node, negate.negate(other_node))))

    def __rsub__(self, other: Qobj | Qsymbolic | complex) -> Qsymbolic:
        if other == 0:
            if self._node is None:
                return self
            return Qsymbolic(negate.negate(self._node))
        other_node = to_node(other)
        if self._node is None:
            return Qsymbolic(other_node)
        return Qsymbolic(sum.from_terms((other_node, negate.negate(self._node))))

    # TODO: __mul__
    # TODO: __rmul__

    def __matmul__(self, other: Qobj | Qsymbolic) -> Qsymbolic:
        # TODO: Support scalars
        if self._node is None:
            raise ValueError("An empty Qsymbolic does not support multiplication.")
        other_node = to_node(other)
        return Qsymbolic(matmul.from_factors((self._node, other_node)))

    def __and__(self, other: Qobj | Qsymbolic) -> Qsymbolic:
        if self._node is None:
            raise ValueError("An empty Qsymbolic does not support tensor products.")
        other_node = to_node(other)
        return Qsymbolic(tensor.from_subspaces((self._node, other_node)))

    def __truediv__(self, other: complex) -> Qsymbolic:
        if other == 0:
            raise ZeroDivisionError("division by zero")
        return self.__mul__(1 / other)

    def __neg__(self) -> Qsymbolic:
        if self._node is None:
            return self
        return Qsymbolic(negate.negate(self._node))

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._node == other._node

    # TODO: __pow__

    def dag(self) -> Qsymbolic:
        if self._node is None:
            return self
        return Qsymbolic(adjoint.adjoint(self._node))

    def conj(self) -> Qsymbolic:
        if self._node is None:
            return self
        return Qsymbolic(conjugate.conjugate(self._node))

    def trans(self) -> Qsymbolic:
        if self._node is None:
            return self
        return Qsymbolic(transpose.transpose(self._node))
