"""
Tests for qutip.symbolic.nodes.transpose.
"""

import pytest

import qutip
from qutip.symbolic.nodes import to_node, transpose


class TestTranspose:
    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(2 + 2j, id="constant"),
            pytest.param(qutip.sigmax(), id="qobj"),
        ],
    )
    def test_simple_values(self, value):
        value_node = to_node(value)
        node = transpose.transpose(value_node)

        assert node.stype == "transpose"
        assert node.dims is value_node.dims
        assert node.args == (value_node,)
        assert node.metadata is None
