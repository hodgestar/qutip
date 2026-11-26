"""
A node that tranposes its value.
"""

from __future__ import annotations

from .core import SymbolicArgsType, SymbolicNode, SymbolicType

STYPE = SymbolicType.TRANSPOSE.value
ARGS_TYPE = SymbolicArgsType.TRANSPOSE


def transpose(
    node: SymbolicNode,
    *,
    metadata: dict | None = None,
):
    """
    Construct an TRANSPOSE node from a node to transpose.

    Parameters
    ----------
    node: SymbolicNode
       The node to transpose.
    metadata: dict or None
       The metadata for the node.
    """
    return SymbolicNode(
        stype=STYPE,
        dims=node.dims,
        args=ARGS_TYPE((node,)),
        metadata=metadata,
    )
