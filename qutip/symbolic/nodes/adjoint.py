"""
A node that performs the adjoint of its value.
"""

from __future__ import annotations

from .core import SymbolicArgsType, SymbolicNode, SymbolicType

STYPE = SymbolicType.ADJOINT.value
ARGS_TYPE = SymbolicArgsType.ADJOINT


def adjoint(
    node: SymbolicNode,
    *,
    metadata: dict | None = None,
):
    """
    Construct an ADJOINT node from a node to perform the adjoint on.

    Parameters
    ----------
    node: SymbolicNode
       The node to perform the adjoint on.
    metadata: dict or None
       The metadata for the node.
    """
    return SymbolicNode(
        stype=STYPE,
        dims=node.dims,
        args=ARGS_TYPE((node,)),
        metadata=metadata,
    )
