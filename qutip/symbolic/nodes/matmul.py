"""
A node that stores a matrix multiplication product over other symbolic nodes.
"""

from __future__ import annotations

import typing

from qutip.core.dimensions import Field
from .core import SymbolicType, SymbolicArgsType, SymbolicNode

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

STYPE = SymbolicType.MATMUL.value
ARGS_TYPE = SymbolicArgsType.MATMUL


def from_factors(
    factors: Iterable[SymbolicNode],
    *,
    metadata: dict | None = None,
):
    """
    Construct a MATMUL node from products.

    Parameters
    ----------
    factors: Iterable[SymbolicNode]
       The nodes that make up the matrix multiplication product.
    metadata: dict or None
       The metadata for the node.

    Note
    ----
    There must be at least one factor so that the dimensions of
    the product can be determined. The dimensions of the factors must
    be compatible.

    Dimensions are compatible if the input and output dimensions of
    adjacent factors are the same, or if the dimension is `Field`.
    `Field` dimensions are treated as a scalar times the identify of
    the appropriate size. If all factors have dimension `Field` the
    dimension of the product is `Field`.
    """
    factors = tuple(factors)
    if not factors:
        raise ValueError("A SymbolicNode.MATMUL must contain at least one factor.")
    # TODO: Fix dimension checking, this is just copied from SUM:
    non_field_dimensions = {
        dims for node in factors if type(dims := node.dims) is not Field
    }
    if not non_field_dimensions:
        dims = Field()
    elif len(non_field_dimensions) == 1:
        dims = tuple(non_field_dimensions)[0]
    else:
        raise ValueError(
            f"A SymbolicNode.MATMUL must have factors with compatible dimensions."
            f" The following dimensions are incompatible: {non_field_dimensions}"
        )
    return SymbolicNode(
        stype=STYPE,
        dims=factors[0].dims,
        args=ARGS_TYPE(factors),
        metadata=metadata,
    )
