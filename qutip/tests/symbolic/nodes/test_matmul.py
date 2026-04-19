"""
Tests for qutip.symbolic.nodes.matmul.
"""

import pytest

import qutip
from qutip.core.dimensions import Dimensions
from qutip.symbolic.nodes import to_node, matmul


class TestFromFactors:
    def test_matmul_node_with_one_factor(self):
        factors = [
            to_node(qutip.sigmax()),
        ]
        node = matmul.from_factors(factors)

        assert node.stype == "matmul"
        assert node.dims is factors[0].dims
        assert node.args == tuple(factors)
        assert node.metadata is None

    def test_matmul_node_with_two_terms(self):
        factors = [
            to_node(qutip.sigmax()),
            to_node(qutip.sigmay()),
        ]
        node = matmul.from_factors(factors)

        assert node.stype == "matmul"
        assert node.dims == Dimensions(factors[0].dims.from_, factors[-1].dims.to_)
        assert node.args == tuple(factors)
        assert node.metadata is None

    def test_matmul_node_preserves_tuple_identity(self):
        factors = (to_node(qutip.sigmax()),)
        node = matmul.from_factors(factors)

        assert node.args is factors

    def test_matmul_node_with_zero_terms(self):
        with pytest.raises(ValueError) as err:
            matmul.from_factors([])

        assert (
            str(err.value) == "A SymbolicNode.MATMUL must contain at least one factor."
        )
