"""
Tests for qutip.symbolic.nodes.matmul.
"""

import pytest

import qutip
from qutip.core.dimensions import Dimensions, Field
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

    @pytest.mark.parametrize(
        ("factors", "expected_dims"),
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
    def test_matmul_dims(self, factors, expected_dims):
        factors = [to_node(f) for f in factors]
        node = matmul.from_factors(factors)
        if isinstance(expected_dims, list):
            expected_dims = Dimensions(expected_dims)

        assert node.dims == expected_dims

    @pytest.mark.parametrize(
        ("factors", "left_dims", "right_dims"),
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
    def test_matmul_dims_errors(self, factors, left_dims, right_dims):
        factors = [to_node(f) for f in factors]
        with pytest.raises(TypeError) as err:
            matmul.from_factors(factors)
        assert str(err.value) == f"incompatible dimensions {left_dims} and {right_dims}"

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
