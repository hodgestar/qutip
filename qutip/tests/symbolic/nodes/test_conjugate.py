"""
Tests for qutip.symbolic.nodes.conjugate.
"""

import pytest

import qutip
from qutip.symbolic.nodes import conjugate, to_node


class TestConjugate:
    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(2 + 2j, id="constant"),
            pytest.param(qutip.sigmax(), id="qobj"),
        ],
    )
    def test_simple_values(self, value):
        value_node = to_node(value)
        node = conjugate.conjugate(value_node)

        assert node.stype == "conjugate"
        assert node.dims is value_node.dims
        assert node.args == (value_node,)
        assert node.metadata is None
