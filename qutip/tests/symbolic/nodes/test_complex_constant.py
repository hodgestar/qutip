"""
Tests for qutip.symbolic.nodes.complex_constant.
"""

import pytest

from qutip.core.dimensions import Field
from qutip.symbolic.nodes import complex_constant, to_node


class TestFromQobj:
    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(2 + 2j, id="complex"),
            pytest.param(1, id="int"),
            pytest.param(1.5, id="float"),
        ],
    )
    def test_simple_values(self, value):
        node = complex_constant.from_number(value)

        assert node.stype == "complex_constant"
        assert node.dims is Field()
        assert node.args.value == complex(value)
        assert node.metadata is None


class TestToNode:
    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(2 + 2j, id="complex"),
            pytest.param(1, id="int"),
            pytest.param(1.5, id="float"),
        ],
    )
    def test_simple_values(self, value):
        node = to_node(value)
        assert node == complex_constant.from_number(value)
