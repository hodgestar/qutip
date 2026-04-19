"""
A node that stores a complex scalar constant.
"""

from __future__ import annotations

from qutip.core.dimensions import Field
from .core import SymbolicType, SymbolicArgsType, SymbolicNode, to_node

STYPE = SymbolicType.COMPLEX_CONSTANT.value
ARGS_TYPE = SymbolicArgsType.COMPLEX_CONSTANT

# We manually register the types in order to support Python 3.10
# where singledispatch.register does not support unions:


@to_node.register(complex)
@to_node.register(float)
@to_node.register(int)
def from_number(
    obj: complex | float | int,
    *,
    metadata: dict | None = None,
):
    """
    Construct a COMPLEX_CONSTANT node from a numeric value.

    Parameters
    ----------
    obj: complex | float | int
       The value to construct the node from.
    metadata: dict or None
       The metadata for the node.
    """
    return SymbolicNode(
        stype=STYPE,
        dims=Field(),
        args=ARGS_TYPE(value=complex(obj)),
        metadata=metadata,
    )
