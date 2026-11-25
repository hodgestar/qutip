"""
Core infrastructure for symbolic nodes.
"""

from __future__ import annotations

import collections
import enum
import functools

SymbolicNode = collections.namedtuple(
    "SymbolicNode",
    field_names=["stype", "dims", "args", "metadata"],
    defaults={"args": (), "metadata": None},
)

# TODO: Currently .dims may be either a Field or a Dimension
#       Is this a good idea? Is this the right way?
#       If yes, the type information in the docstring should be updated to match.
#       If not, fix Qsymbolic.type.

# TODO: Look at supporting all the important / common operators from qutip.core.operator.

# TODO: Look at supporting coefficient functions, including some indication of the behaviour
#       of the function around a particular set of parameters -- e.g. `t`.
#       I.e. adaptive timesteps for the solver.
#
#       How far can we get with SymPy core (https://docs.sympy.org/latest/modules/core.html)
#       and symjit (https://github.com/siravan/symjit)?

SymbolicNode.__doc__ = """
A node in the symbolic operations graph.

Parameters
----------
stype: SymbolicType
   The kind of node.
dims: Dimensions
   The dimensions of the node.
args: tuple
    A tuple of immutable arguments.
    Nodes of a given `stype` may supply
    a fixed `namedtuple` for the args.
metadata: dict or None
   A dictionary of metadata.

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
    # TODO: Rename complex_coefficient to coefficient
    CONSTANT = "constant"
    COMPLEX_COEFFICIENT = "complex_coefficient"

    # Single-child operation nodes:

    NEGATE = "negate"

    # Multi-child operation nodes:

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
    CONSTANT = collections.namedtuple(
        "ConstantArgsType",
        field_names=["value"],
    )

    # Single-child operation nodes:

    NEGATE = tuple[SymbolicNode]

    # Multi-child operation nodes:

    SUM = tuple[SymbolicNode, ...]
    MATMUL = tuple[SymbolicNode, ...]
    TENSOR = tuple[SymbolicNode, ...]


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
    raise TypeError(
        f"Object {obj!r}, of type {type(obj)}, could not be converted to a SymbolicNode."
    )


@to_node.register
def from_symbolic_node(
    obj: SymbolicNode,
    *,
    metadata: dict | None = None,
):
    """
    Convert a SymbolicNode to a SymbolicNode.

    If the supplied metadata is None, the node is returned without copying.
    Otherwise a copy of the node with the metadata *replaced* is returned.

    Parameters
    ----------
    obj: SymbolicNode
       The Qobj to construct the node from.
    metadata: dict or None
       The metadata for the node.
    """
    if metadata is None:
        return obj
    return SymbolicNode(
        stype=obj.stype,
        dims=obj.dims,
        args=obj.args,
        metadata=metadata,
    )


# TODO: We need an easy way to:
# - Register new symbolic types
# - Register new symbolic argument types
# - Dispatch based on stype
# - Visit a tree of nodes
