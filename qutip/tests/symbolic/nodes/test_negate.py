"""
Tests for qutip.symbolic.nodes.negate.
"""

import pytest

import qutip
from qutip.symbolic.nodes import negate, to_node


class TestNegate:
    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(2 + 2j, id="complex_constant"),
            pytest.param(qutip.sigmax(), id="qobj"),
        ],
    )
    def test_simple_values(self, value):
        value_node = to_node(value)
        node = negate.negate(value_node)

        assert node.stype == "negate"
        assert node.dims is value_node.dims
        assert node.args == (value_node,)
        assert node.metadata is None
