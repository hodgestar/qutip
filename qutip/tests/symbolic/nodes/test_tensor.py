"""
Tests for qutip.symbolic.nodes.tensor.
"""

import pytest

import qutip
from qutip.core import tensor as tensor_qobj
from qutip.core.dimensions import Dimensions, Field
from qutip.symbolic.nodes import to_node, tensor


class TestFromSubspaces:
    def test_tensor_node_with_one_subspace(self):
        subspace_qobjs = [qutip.sigmax()]
        qobj = tensor_qobj(*subspace_qobjs)

        subspaces = [to_node(s) for s in subspace_qobjs]
        node = tensor.from_subspaces(subspaces)

        assert node.stype == "tensor"
        assert node.dims is qobj._dims
        assert node.args == tuple(subspaces)
        assert node.metadata is None

    def test_tensor_node_with_two_subspaces(self):
        subspace_qobjs = [qutip.sigmax(), qutip.sigmay()]
        qobj = tensor_qobj(*subspace_qobjs)

        subspaces = [to_node(s) for s in subspace_qobjs]
        node = tensor.from_subspaces(subspaces)

        assert node.stype == "tensor"
        assert node.dims == qobj._dims
        assert node.args == tuple(subspaces)
        assert node.metadata is None

    @pytest.mark.parametrize(
        ("subspaces", "expected_dims"),
        [
            pytest.param((qutip.sigmax(),), [[2], [2]], id="oper"),
            pytest.param((qutip.sigmax(),) * 2, [[2, 2], [2, 2]], id="oper-oper"),
            pytest.param(
                (qutip.sigmax(),) * 3, [[2, 2, 2], [2, 2, 2]], id="oper-oper-oper"
            ),
        ],
    )
    def test_tensor_dims(self, subspaces, expected_dims):
        subspaces = [to_node(s) for s in subspaces]
        node = tensor.from_subspaces(subspaces)

        expected_dims = Dimensions(expected_dims)

        assert node.dims == expected_dims

    @pytest.mark.parametrize(
        ("subspaces", "field_dimensions"),
        [
            pytest.param(
                (5,),
                "[0]",
                id="field",
            ),
            pytest.param(
                (qutip.create(3), 5),
                "[1]",
                id="oper-field",
            ),
            pytest.param(
                (5, qutip.create(3)),
                "[0]",
                id="field-oper",
            ),
            pytest.param(
                (qutip.create(3), 5, qutip.sigmax()),
                "[1]",
                id="oper-field-oper",
            ),
            pytest.param(
                (qutip.create(3), 5, qutip.sigmax(), 7),
                "[1, 3]",
                id="oper-field-oper-field",
            ),
        ],
    )
    def test_tensor_field_dims_errors(self, subspaces, field_dimensions):
        subspaces = [to_node(s) for s in subspaces]
        with pytest.raises(TypeError) as err:
            tensor.from_subspaces(subspaces)
        assert str(err.value) == (
            f"A SymbolicNode.TENSOR must not have subspaces with field dimensions."
            f" The following dimensions are fields: {field_dimensions}"
        )

    def test_tensor_node_preserves_tuple_identity(self):
        subspaces = (to_node(qutip.sigmax()),)
        node = tensor.from_subspaces(subspaces)

        assert node.args is subspaces

    def test_tensor_node_with_zero_subspaces(self):
        with pytest.raises(ValueError) as err:
            tensor.from_subspaces([])

        assert (
            str(err.value)
            == "A SymbolicNode.TENSOR must contain at least one subspace."
        )
