"""
A node that stores a tensor product over other symbolic nodes.
"""

from __future__ import annotations

import typing

from qutip.core.dimensions import Field
from .core import SymbolicType, SymbolicArgsType, SymbolicNode

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

STYPE = SymbolicType.TENSOR.value
ARGS_TYPE = SymbolicArgsType.TENSOR

# TODO: Support flattening of tensors of tensors via tensor(a, b) method.

# TODO: Decide what the compatibility requirements should be for tensor
#       subspaces by looking at, e.g., the relevant parts of qutip's
#       dimensions support.

def from_subspaces(
    subspaces: Iterable[SymbolicNode],
    *,
    metadata: dict | None = None,
):
    """
    Construct a TENSOR node from subspaces.

    Parameters
    ----------
    subspaces: Iterable[SymbolicNode]
       The nodes that make up the tensor product.
    metadata: dict or None
       The metadata for the node.

    Note
    ----
    There must be at least one subspace so that the dimensions of
    the product can be determined. The dimensions of the subspaces
    must be compatible and not contain fields.
    """
    subspaces = tuple(subspaces)
    if not subspaces:
        raise ValueError("A SymbolicNode.TENSOR must contain at least one subspace.")

    field_dimensions = [
        dims for node in subspaces if type(dims := node.dims) is Field
    ]
    if field_dimensions:
        raise ValueError(
            f"A SymbolicNode.TENSOR must not have subspaces with field dimensions."
            f" The following dimensions are fields: {field_dimensions}"
        )

    dims = subspaces[0].dims
    for node in subspaces[1:]:
        dims = dims & node.dims

    return SymbolicNode(
        stype=STYPE,
        dims=dims,
        args=ARGS_TYPE(subspaces),
        metadata=metadata,
    )
