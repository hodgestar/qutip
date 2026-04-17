"""
Core of the symbolic quantum object representation.
"""

from __future__ import annotations

import collections
import enum
import typing

if typing.TYPE_CHECKING:
    from collections.abc import Iterable
    from qutip import Qobj


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

    QOBJ = "qobj"
    SUM = "sum"


class SymbolicArgsType:
    """
    Enumeration of the type of the `args` supplied to a `SymbolicNode` of a given
    `SymbolicType`.

    All argument types must be either tuples or namedtuples.
    """

    QOBJ = collections.namedtuple(
        "QobjNodeArgsType", field_names=["data", "isherm", "isunitary"]
    )
    SUM = tuple


# TODO: We need an easy way to:
# - Register new symbolic types
# - Register new symbolic argument types
# - Dispatch based on stype


class QSymbolic:
    """
    The symbolic equivalent of Qobj and QobjEvo.
    """


def qobj_node(
    qobj: Qobj,
    *,
    metadata: dict | None = None,
):
    """
    A node that stores a constant quantum object.

    Parameters
    ----------
    qobj: Qobj
       The Qobj to construct the node from.
    metadata: dict or None
       The metadata for the node.
    """
    return SymbolicNode(
        stype=SymbolicType.QOBJ.value,
        dims=qobj._dims,
        args=SymbolicArgsType.QOBJ(qobj.data, qobj._isherm, qobj._isunitary),
        metadata=metadata,
    )


def sum_node(
    terms: Iterable,
    *,
    metadata: dict | None = None,
):
    """
    A node that stores a sum over other symbolic nodes.

    Parameters
    ----------
    terms: Iterable
       The nodes that make up the sum.
    metadata: dict or None
       The metadata for the node.
    """
    terms = tuple(terms)
    if not terms:
        raise ValueError("A SymbolicNode.SUM must contain at least one term.")
    return SymbolicNode(
        stype=SymbolicType.SUM.value,
        dims=terms[0].dims,
        args=SymbolicArgsType.SUM(terms),
        metadata=metadata,
    )


# TODO: Move tests into their own file.

import pytest
import qutip


def test_qobj_node():
    op = qutip.sigmax()
    node = qobj_node(op)

    assert node.stype == "qobj"
    assert node.dims is op._dims
    assert node.args.data is op.data
    assert node.args.isherm == op._isherm
    assert node.args.isunitary == op._isunitary
    assert node.metadata is None


def test_sum_node_with_one_term():
    terms = [
        qobj_node(qutip.sigmax()),
    ]
    node = sum_node(terms)

    assert node.stype == "sum"
    assert node.dims is terms[0].dims
    assert node.args == tuple(terms)
    assert node.metadata is None


def test_sum_node_with_two_terms():
    terms = [
        qobj_node(qutip.sigmax()),
        qobj_node(qutip.sigmay()),
    ]
    node = sum_node(terms)

    assert node.stype == "sum"
    assert node.dims is terms[0].dims
    assert node.args == tuple(terms)
    assert node.metadata is None


def test_sum_node_preserves_tuple_identity():
    terms = (qobj_node(qutip.sigmax()),)
    node = sum_node(terms)

    assert node.args is terms


def test_sum_node_with_zero_terms():
    with pytest.raises(ValueError) as err:
        sum_node([])

    assert str(err.value) == "A SymbolicNode.SUM must contain at least one term."
