"""
A node that conjugates its value.
"""

from __future__ import annotations

from .core import SymbolicArgsType, SymbolicNode, SymbolicType

STYPE = SymbolicType.CONJUGATE.value
ARGS_TYPE = SymbolicArgsType.CONJUGATE


def conjugate(
    node: SymbolicNode,
    *,
    metadata: dict | None = None,
):
    """
    Construct an CONJUGATE node from a node to conjugate.

    Parameters
    ----------
    node: SymbolicNode
       The node to conjugate.
    metadata: dict or None
       The metadata for the node.
    """
    return SymbolicNode(
        stype=STYPE,
        dims=node.dims,
        args=ARGS_TYPE((node,)),
        metadata=metadata,
    )
