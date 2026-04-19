"""
Core infrastructure for symbolic nodes.
"""

from __future__ import annotations

import collections
import enum
import functools

SymbolicNode = collections.namedtuple(
    "SymbolicNode",
    field_names=["stype", "dims", "metadata", "args"],
    defaults={"metadata": None, "args": ()},
)


SymbolicNode.__doc__ = """
A node in the symbolic operations graph.

Parameters
----------
stype: SymbolicType
   The kind of node.
dims: Dimensions
   The dimensions of the node.
metadata: dict or None
   A dictionary of metadata.
args: tuple
    A tuple of immutable arguments.
    Nodes of a given `stype` may supply
    a fixed `namedtuple` for the args.

The interpretation of the node arguments is
dependented on the type of node. All arguments
must be immutable as nodes may be re-used within
the symbolic graph.

A common pattern is for `args` to be a tuple of
other `SymbolicNode` instances.

Nodes are stored as tuples to reduce their memory overhead.
It is expected that large symbolic representations will
consist of many nodes.
"""


class SymbolicType(enum.Enum):
    """
    Enumeration of types of symbolic nodes for use as
    values for `SymbolicNode.stype`.
    """

    # Leaf nodes:

    QOBJ = "qobj"
    COMPLEX_CONSTANT = "complex_constant"
    COMPLEX_COEFFICIENT = "complex_coefficient"

    # Operation nodes:

    SUM = "sum"
    MATMUL = "matmul"
    TENSOR = "tensor"


class SymbolicArgsType:
    """
    Enumeration of the type of the `args` supplied to a `SymbolicNode` of a given
    `SymbolicType`.

    All argument types must be either tuples or namedtuples.
    """

    # TODO: It would be very helpful to specify the types of the fields
    #       in the arguments here.

    # Leaf nodes:

    QOBJ = collections.namedtuple(
        "QobjNodeArgsType",
        field_names=["data", "isherm", "isunitary"],
    )
    COMPLEX_CONSTANT = collections.namedtuple(
        "ComplexConstantArgsType",
        field_names=["value"],
    )

    # Operation nodes:

    SUM = tuple[SymbolicNode]
    MATMUL = tuple[SymbolicNode]


@functools.singledispatch
def to_node(obj: object, *, metadata: dict | None = None):
    """
    Attempt to convert an object to a `SymbolicNode`.

    Parameters
    ----------
    obj: object
        The object to construct the node from.
    metadata: dict or None
        The metadata for the node.
    """
    if type(obj) is SymbolicNode:
        return obj
    raise TypeError(
        f"Object {obj!r}, of type {type(obj)}, could not be converted to a SymbolicNode."
    )


# TODO: We need an easy way to:
# - Register new symbolic types
# - Register new symbolic argument types
# - Dispatch based on stype
# - Visit a tree of nodes
