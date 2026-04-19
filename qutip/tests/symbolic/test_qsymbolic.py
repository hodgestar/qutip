"""
Tests for qutip.symbolic.qsymbolic.
"""

import pytest

import qutip
from qutip.symbolic.qsymbolic import Qsymbolic
from qutip.symbolic.nodes import to_node


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

    def test_add_with_no_node(self):
        H = Qsymbolic() + 1
        assert H._node == to_node(1)

    def test_add_with_zero(self):
        H = Qsymbolic()
        H_plus_0 = H + 0
        assert H is H_plus_0

    def test_radd_with_no_node(self):
        H = 1 + Qsymbolic()
        assert H._node == to_node(1)

    def test_radd_with_zero(self):
        H = Qsymbolic()
        H_plus_0 = 0 + H
        assert H is H_plus_0
