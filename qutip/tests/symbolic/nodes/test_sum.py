"""
Tests for qutip.symbolic.nodes.sum.
"""

import pytest

import qutip
from qutip.symbolic.nodes import to_node, sum


class TestFromTerms:
    def test_sum_node_with_one_term(self):
        terms = [
            to_node(qutip.sigmax()),
        ]
        node = sum.from_terms(terms)

        assert node.stype == "sum"
        assert node.dims is terms[0].dims
        assert node.args == tuple(terms)
        assert node.metadata is None

    def test_sum_node_with_two_terms(self):
        terms = [
            to_node(qutip.sigmax()),
            to_node(qutip.sigmay()),
        ]
        node = sum.from_terms(terms)

        assert node.stype == "sum"
        assert node.dims is terms[0].dims
        assert node.args == tuple(terms)
        assert node.metadata is None

    def test_sum_node_preserves_tuple_identity(self):
        terms = (to_node(qutip.sigmax()),)
        node = sum.from_terms(terms)

        assert node.args is terms

    def test_sum_node_with_zero_terms(self):
        with pytest.raises(ValueError) as err:
            sum.from_terms([])

        assert str(err.value) == "A SymbolicNode.SUM must contain at least one term."
