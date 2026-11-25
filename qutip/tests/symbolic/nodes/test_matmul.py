"""
Tests for qutip.symbolic.nodes.matmul.
"""

import pytest

import qutip
from qutip.core.dimensions import Dimensions, Field
from qutip.symbolic.nodes import matmul, to_node

# Helpful constants

qobj_2x3 = qutip.Qobj([[1, 2, 3], [4, 5, 6]])
qobj_3x2 = qutip.Qobj([[1, 2], [3, 4], [5, 6]])
sx = qutip.sigmax()
sy = qutip.sigmay()


class TestFromFactors:
    def test_matmul_node_with_one_factor(self):
        factors = [
            to_node(sx),
        ]
        node = matmul.from_factors(factors)

        assert node.stype == "matmul"
        assert node.dims is factors[0].dims
        assert node.args == tuple(factors)
        assert node.metadata is None

    def test_matmul_node_with_two_terms(self):
        factors = [
            to_node(sx),
            to_node(sy),
        ]
        node = matmul.from_factors(factors)

        assert node.stype == "matmul"
        assert node.dims == Dimensions(factors[0].dims.from_, factors[-1].dims.to_)
        assert node.args == tuple(factors)
        assert node.metadata is None

    @pytest.mark.parametrize(
        ("factors", "expected_dims"),
        [
            pytest.param((sx,), [[2], [2]], id="oper"),
            pytest.param((sx, sy), [[2], [2]], id="oper-oper"),
            pytest.param((sx, sy, sx), [[2], [2]], id="oper-oper-oper"),
            pytest.param((5,), Field(), id="field"),
            pytest.param((5, 3), Field(), id="field-field"),
            pytest.param((5, 3, 2), Field(), id="field-field-field"),
            pytest.param((sx, 4), [[2], [2]], id="oper-field"),
            pytest.param((3, sx), [[2], [2]], id="field-oper"),
            pytest.param((qobj_2x3,), [[2], [3]], id="oper-non-sqyare"),
            pytest.param((qobj_2x3, qobj_3x2), [[2], [2]], id="oper-oper-non-square"),
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
                (qutip.create(3), sx),
                [[3], [3]],
                [[2], [2]],
                id="oper-oper",
            ),
            pytest.param(
                (qutip.create(3), 5, sx),
                [[3], [3]],
                [[2], [2]],
                id="oper-field-oper",
            ),
            pytest.param(
                (qobj_2x3, qobj_2x3), [[2], [3]], [[2], [3]], id="oper-oper-non-square"
            ),
        ],
    )
    def test_matmul_dims_errors(self, factors, left_dims, right_dims):
        factors = [to_node(f) for f in factors]
        with pytest.raises(ValueError) as err:
            matmul.from_factors(factors)
        assert str(err.value) == (
            f"A SymbolicNode.MATMUL must have factors with compatible dimensions."
            f" The following dimensions are incompatible:"
            f" incompatible dimensions {left_dims} and {right_dims}"
        )

    def test_matmul_node_preserves_tuple_identity(self):
        factors = (to_node(sx),)
        node = matmul.from_factors(factors)

        assert node.args is factors

    def test_matmul_node_with_zero_terms(self):
        with pytest.raises(ValueError) as err:
            matmul.from_factors([])

        assert (
            str(err.value) == "A SymbolicNode.MATMUL must contain at least one factor."
        )
