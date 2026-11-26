"""
Support for converting a symbolic tree to a qobj.
"""

import functools
import operator

from qutip import Qobj
from qutip.core import tensor
from qutip.core.dimensions import Field

from ..nodes import SymbolicNode
from .core import stypedispatch


@stypedispatch
def to_qobj(node: SymbolicNode):
    raise TypeError(f"SymbolicNode with stype={node.stype!r} not supported by to_qobj.")


_from_node = to_qobj.from_node


@to_qobj.register("qobj")
def _from_qobj(node: SymbolicNode):
    return Qobj(
        node.args.data,
        dims=node.dims,
        isherm=node.args.isherm,
        isunitary=node.args.isunitary,
    )


@to_qobj.register("constant")
def _from_complex_constant(node: SymbolicNode):
    return node.args.value


@to_qobj.register("negate")
def _from_negate(node: SymbolicNode):
    return -_from_node(node.args[0])


@to_qobj.register("sum")
def _from_sum(node: SymbolicNode):
    assert node.args, "SymbolicNode.SUM has empty tuple of terms"
    return sum(_from_node(term) for term in node.args)


@to_qobj.register("matmul")
def _from_matmul(node: SymbolicNode):
    assert node.args, "SymbolicNode.MATMUL has empty tuple of factors"
    # We need to loop ourselves here because any multiplication step
    # might return a scalar:
    result = _from_node(node.args[0])
    for factor in node.args[1:]:
        obj = _from_node(factor)
        if not isinstance(result, Qobj) or not isinstance(obj, Qobj):
            result = result * obj
        else:
            result = result @ obj
    return result


@to_qobj.register("tensor")
def _from_tensor(node: SymbolicNode):
    assert node.args, "SymbolicNode.TENSOR has empty tuple of subspaces"
    return tensor(_from_node(subspace) for subspace in node.args)
