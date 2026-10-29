"""
A node that stores a tensor product over other symbolic nodes.
"""

from __future__ import annotations

import typing

from qutip.core.dimensions import Compound, Dimensions, Field
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
        i for i, node in enumerate(subspaces) if type(node.dims) is Field
    ]
    if field_dimensions:
        raise TypeError(
            f"A SymbolicNode.TENSOR must not have subspaces with field dimensions."
            f" The following dimensions are fields: {field_dimensions}"
        )

    dims_l = [s.dims[0] for s in subspaces]
    dims_r = [s.dims[1] for s in subspaces]
    dims = Dimensions([dims_l, dims_r])

    return SymbolicNode(
        stype=STYPE,
        dims=dims,
        args=ARGS_TYPE(subspaces),
        metadata=metadata,
    )
