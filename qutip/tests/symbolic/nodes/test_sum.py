"""
Tests for qutip.symbolic.nodes.sum.
"""

import pytest

import qutip
from qutip.core.dimensions import Dimensions, Field
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

    @pytest.mark.parametrize(
        ("terms", "expected_dims"),
        [
            pytest.param((qutip.sigmax(),), [[2], [2]], id="oper"),
            pytest.param((qutip.sigmax(),) * 2, [[2], [2]], id="oper-oper"),
            pytest.param((qutip.sigmax(),) * 3, [[2], [2]], id="oper-oper-oper"),
            pytest.param((5,), Field(), id="field"),
            pytest.param((5, 3), Field(), id="field-field"),
            pytest.param((5, 3, 2), Field(), id="field-field-field"),
            pytest.param((qutip.sigmax(), 4), [[2], [2]], id="oper-field"),
            pytest.param((3, qutip.sigmax()), [[2], [2]], id="field-oper"),
        ],
    )
    def test_sum_dims(self, terms, expected_dims):
        terms = [to_node(t) for t in terms]
        node = sum.from_terms(terms)
        if isinstance(expected_dims, list):
            expected_dims = Dimensions(expected_dims)

        assert node.dims == expected_dims

    @pytest.mark.parametrize(
        ("terms", "left_dims", "right_dims"),
        [
            pytest.param(
                (qutip.create(3), qutip.sigmax()),
                [[3], [3]],
                [[2], [2]],
                id="oper-oper",
            ),
            pytest.param(
                (qutip.create(3), 5, qutip.sigmax()),
                [[3], [3]],
                [[2], [2]],
                id="oper-field-oper",
            ),
        ],
    )
    def test_sum_dims_errors(self, terms, left_dims, right_dims):
        terms = [to_node(t) for t in terms]
        with pytest.raises(TypeError) as err:
            sum.from_terms(terms)
        assert str(err.value) == (
            f"A SymbolicNode.SUM must have terms with compatible dimensions."
            f" The following dimensions are incompatible:"
            f" {left_dims}, {right_dims}"
        )

    def test_sum_node_preserves_tuple_identity(self):
        terms = (to_node(qutip.sigmax()),)
        node = sum.from_terms(terms)

        assert node.args is terms

    def test_sum_node_with_zero_terms(self):
        with pytest.raises(ValueError) as err:
            sum.from_terms([])

        assert str(err.value) == "A SymbolicNode.SUM must contain at least one term."
