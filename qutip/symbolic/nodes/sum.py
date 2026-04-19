"""
A node that stores a sum over other symbolic nodes.
"""

from __future__ import annotations

import typing

from qutip.core.dimensions import Field
from .core import SymbolicType, SymbolicArgsType, SymbolicNode

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

STYPE = SymbolicType.SUM.value
ARGS_TYPE = SymbolicArgsType.SUM


def from_terms(
    terms: Iterable[SymbolicNode],
    *,
    metadata: dict | None = None,
):
    """
    Construct a SUM node from terms.

    Parameters
    ----------
    terms: Iterable[SymbolicNode]
       The nodes that make up the sum.
    metadata: dict or None
       The metadata for the node.

    Note
    ----
    There must be at least one term so that the dimensions of
    the sum can be determined. The dimensions of the terms must
    be compatible.

    Dimensions are compatible if they are the same or the dimension
    is `Field`. `Field` dimensions are treated as a scalar times
    the identify of the appropriate size. If all terms have dimension
    `Field` the dimension of the sum is `Field`.
    """
    terms = tuple(terms)
    if not terms:
        raise ValueError("A SymbolicNode.SUM must contain at least one term.")
    non_field_dimensions = {
        dims for node in terms if type(dims := node.dims) is not Field
    }
    if not non_field_dimensions:
        dims = Field()
    elif len(non_field_dimensions) == 1:
        dims = tuple(non_field_dimensions)[0]
    else:
        raise ValueError(
            f"A SymbolicNode.SUM must have terms with compatible dimensions."
            f" The following dimensions are incompatible: {non_field_dimensions}"
        )
    return SymbolicNode(
        stype=STYPE,
        dims=terms[0].dims,
        args=ARGS_TYPE(terms),
        metadata=metadata,
    )
