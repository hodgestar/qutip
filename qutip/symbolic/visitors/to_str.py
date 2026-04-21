"""
Support for printing a symbolic tree as a str.
"""

from .core import stypedispatch
from ..nodes import SymbolicNode

# TODO: It would be more efficient to build a list of lines and
#       the concatenate the lines at the end. This requires
#       add functionality to post-process the result. Alternatively
#       we could just return the list of strings.


@stypedispatch
def to_str(node: SymbolicNode):
    raise TypeError(f"SymbolicNode with stype={node.stype!r} no supported by to_str.")


_from_node = to_str.from_node


@to_str.register("qobj")
def _from_qobj(node: SymbolicNode):
    # TODO: print the name of the node if it has one?
    # TODO: print isherm and isunitary
    return f"Qobj: dims={node.dims.as_list()}\ndata=\n{node.data.to_array()}"


@to_str.register("complex_constant")
def _from_complex_constant(node: SymbolicNode):
    value = node.args.value
    if value.imag == 0:
        return f"{value.real:g}"
    if value.real == 0:
        return f"{value.imag:g}j"
    return f"{value:g}"


@to_str.register("negate")
def _from_negate(node: SymbolicNode):
    return f"- {_from_node(node.args[0])}"


@to_str.register("sum")
def _from_sum(node: SymbolicNode):
    assert node.args, "SymbolicNode.SUM has empty tuple of terms"
    return " + ".join(_from_node(term) for term in node.args)


@to_str.register("matmul")
def _from_matmul(node: SymbolicNode):
    assert node.args, "SymbolicNode.MATMUL has empty tuple of factors"
    return " @ ".join(_from_node(factor) for factor in node.args)
