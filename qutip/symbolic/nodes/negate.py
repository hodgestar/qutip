"""
A node that performs unitary negation on its value.
"""

from __future__ import annotations

from .core import SymbolicType, SymbolicArgsType, SymbolicNode

STYPE = SymbolicType.NEGATE.value
ARGS_TYPE = SymbolicArgsType.NEGATE


def negate(
    node: SymbolicNode,
    *,
    metadata: dict | None = None,
):
    """
    Construct a NEG node from a node to negate.

    Parameters
    ----------
    node: SymbolicNode
       The node to negate.
    metadata: dict or None
       The metadata for the node.
    """
    return SymbolicNode(
        stype=STYPE,
        dims=node.dims,
        args=ARGS_TYPE((node,)),
        metadata=metadata,
    )
