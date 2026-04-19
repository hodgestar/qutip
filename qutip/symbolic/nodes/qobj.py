"""
A node that stores a constant quantum object.
"""

from __future__ import annotations

from qutip import Qobj
from .core import SymbolicType, SymbolicArgsType, SymbolicNode, to_node

STYPE = SymbolicType.QOBJ.value
ARGS_TYPE = SymbolicArgsType.QOBJ


@to_node.register
def from_qobj(
    obj: Qobj,
    *,
    metadata: dict | None = None,
):
    """
    Construct a QOBJ node from a Qobj instance.

    Parameters
    ----------
    obj: Qobj
       The Qobj to construct the node from.
    metadata: dict or None
       The metadata for the node.
    """
    return SymbolicNode(
        stype=STYPE,
        dims=obj._dims,
        args=ARGS_TYPE(data=obj.data, isherm=obj._isherm, isunitary=obj._isunitary),
        metadata=metadata,
    )
