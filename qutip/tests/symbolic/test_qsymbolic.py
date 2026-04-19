"""
Tests for qutip.symbolic.qsymbolic.
"""

import pytest

import qutip
from qutip.symbolic.qsymbolic import Qsymbolic
from qutip.symbolic.nodes import to_node, negate, sum


class TestQsymbolic:
    def test_create_empty(self):
        H = Qsymbolic()
        assert H._node is None

    def test_create_from_node(self):
        H = Qsymbolic(node := to_node(5))
        assert H._node is node

    def test_dims(self):
        H = Qsymbolic(to_node(5))
        assert H.dims == [1]

    @pytest.mark.parametrize(
        ("value", "expected_type"),
        [
            pytest.param(5, "scalar", id="constant"),
            pytest.param(qutip.sigmax(), "oper", id="oper"),
        ],
    )
    def test_type_complex_constant(self, value, expected_type):
        H = Qsymbolic(to_node(value))
        assert H.type == expected_type

    @pytest.mark.parametrize(
        ("value", "expected_superrep"),
        [
            pytest.param(5, None, id="constant"),
            pytest.param(qutip.sigmax(), None, id="oper"),
            pytest.param(qutip.spre(qutip.sigmax()), "super", id="oper"),
        ],
    )
    def test_superrep(self, value, expected_superrep):
        H = Qsymbolic(to_node(value))
        assert H.superrep == expected_superrep

    def test_data(self):
        H = Qsymbolic()
        with pytest.raises(TypeError) as err:
            H.data
        assert str(err.value) == "QSymbolic does not support direct conversion to data."

    def test_dtype(self):
        H = Qsymbolic()
        with pytest.raises(TypeError) as err:
            H.dtype
        assert str(err.value) == "QSymbolic does not have a dtype."

    def test_to(self):
        H = Qsymbolic()
        with pytest.raises(TypeError) as err:
            H.to("dense")
        assert str(err.value) == "QSymbolic does not have a dtype to alter."

    @pytest.mark.parametrize(
        ("left", "right"),
        [
            pytest.param(5, 1, id="constant-constant"),
            pytest.param(qutip.sigmax(), qutip.sigmay(), id="oper-oper"),
            pytest.param(qutip.sigmax(), 2, id="oper-constant"),
            pytest.param(2, qutip.sigmax(), id="constant-oper"),
            pytest.param(qutip.spre(qutip.sigmax()), 3, id="super-constant"),
            pytest.param(3, qutip.spre(qutip.sigmax()), id="constant-super"),
        ],
    )
    def test_add(self, left, right):
        left_node = to_node(left)
        right_node = to_node(right)
        H = Qsymbolic(left_node) + right
        assert H._node == sum.from_terms((left_node, right_node))

    def test_add_with_no_node(self):
        H = Qsymbolic() + 1
        assert H._node == to_node(1)

    def test_add_with_zero(self):
        H = Qsymbolic()
        H_plus_0 = H + 0
        assert H is H_plus_0

    @pytest.mark.parametrize(
        ("left", "right"),
        [
            pytest.param(5, 1, id="constant-constant"),
            pytest.param(qutip.sigmax(), qutip.sigmay(), id="oper-oper"),
            pytest.param(qutip.sigmax(), 2, id="oper-constant"),
            pytest.param(2, qutip.sigmax(), id="constant-oper"),
            pytest.param(qutip.spre(qutip.sigmax()), 3, id="super-constant"),
            pytest.param(3, qutip.spre(qutip.sigmax()), id="constant-super"),
        ],
    )
    def test_radd(self, left, right):
        left_node = to_node(left)
        right_node = to_node(right)
        H = left + Qsymbolic(right_node)
        assert H._node == sum.from_terms((left_node, right_node))

    def test_radd_with_no_node(self):
        H = 1 + Qsymbolic()
        assert H._node == to_node(1)

    def test_radd_with_zero(self):
        H = Qsymbolic()
        H_plus_0 = 0 + H
        assert H is H_plus_0

    @pytest.mark.parametrize(
        ("left", "right"),
        [
            pytest.param(5, 1, id="constant-constant"),
            pytest.param(qutip.sigmax(), qutip.sigmay(), id="oper-oper"),
            pytest.param(qutip.sigmax(), 2, id="oper-constant"),
            pytest.param(2, qutip.sigmax(), id="constant-oper"),
            pytest.param(qutip.spre(qutip.sigmax()), 3, id="super-constant"),
            pytest.param(3, qutip.spre(qutip.sigmax()), id="constant-super"),
        ],
    )
    def test_sub(self, left, right):
        left_node = to_node(left)
        right_node = to_node(right)
        H = Qsymbolic(left_node) - right
        assert H._node == sum.from_terms((left_node, negate.negate(right_node)))

    def test_sub_with_no_node(self):
        H = Qsymbolic() - 1
        assert H._node == negate.negate(to_node(1))

    def test_sub_with_zero(self):
        H = Qsymbolic()
        H_minus_0 = H - 0
        assert H is H_minus_0

    @pytest.mark.parametrize(
        ("left", "right"),
        [
            pytest.param(5, 1, id="constant-constant"),
            pytest.param(qutip.sigmax(), qutip.sigmay(), id="oper-oper"),
            pytest.param(qutip.sigmax(), 2, id="oper-constant"),
            pytest.param(2, qutip.sigmax(), id="constant-oper"),
            pytest.param(qutip.spre(qutip.sigmax()), 3, id="super-constant"),
            pytest.param(3, qutip.spre(qutip.sigmax()), id="constant-super"),
        ],
    )
    def test_rsub(self, left, right):
        left_node = to_node(left)
        right_node = to_node(right)
        H = left - Qsymbolic(right_node)
        assert H._node == sum.from_terms((left_node, negate.negate(right_node)))

    def test_rsub_with_no_node(self):
        H = 1 - Qsymbolic()
        assert H._node == to_node(1)

    def test_rsub_with_zero(self):
        H = Qsymbolic(to_node(5))
        minus_H = 0 - H
        assert minus_H._node == negate.negate(to_node(5))

    def test_rsub_with_zero_and_no_node(self):
        H = Qsymbolic()
        minus_H = 0 - H
        assert H is minus_H
