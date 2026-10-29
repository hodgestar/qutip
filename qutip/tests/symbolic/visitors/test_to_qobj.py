"""
Tests for qutip.symbolic.visitors.to_qobj.
"""

import pytest

import qutip
from qutip.symbolic import Qsymbolic
from qutip.symbolic.nodes import to_node
from qutip.symbolic.visitors import to_qobj


class TestToQobj:
    def test_empty(self):
        op = Qsymbolic()
        assert to_qobj(op) is None

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            pytest.param(5, 5, id="real"),
            pytest.param(5.1, 5.1, id="real-fraction"),
            pytest.param(5j, 5j, id="imag"),
            pytest.param(5.1j, 5.1j, id="imag-fraction"),
            pytest.param(1 + 5j, 1 + 5j, id="complex"),
            pytest.param(1.2 + 5.3j, 1.2 + 5.3j, id="complex-fraction"),
        ],
    )
    def test_complex_constant(self, value, expected):
        op = Qsymbolic() + value
        assert to_qobj(op) == expected

    @pytest.mark.parametrize(
        ("terms", "expected"),
        [
            pytest.param([1, 2], 3, id="real-real"),
            pytest.param([1j, 2j], 3j, id="imag-imag"),
        ],
    )
    def test_sum(self, terms, expected):
        op = sum([Qsymbolic()] + terms)
        assert to_qobj(op) == expected

    @pytest.mark.parametrize(
        ("factors", "expected"),
        [
            pytest.param(
                [1, 2], 2, id="real-real", marks=pytest.mark.xfail(reason="todo")
            ),
            pytest.param(
                [1j, 2j], 2, id="imag-imag", marks=pytest.mark.xfail(reason="todo")
            ),
        ],
    )
    def test_matmul(self, factors, expected):
        op = Qsymbolic() + factors[0]
        for f in factors[1:]:
            op = op @ f
        assert to_qobj(op) == expected

    @pytest.mark.parametrize(
        ("subspaces", "expected"),
        [
            pytest.param(
                [qutip.sigmax(), qutip.sigmay()],
                qutip.tensor(qutip.sigmax(), qutip.sigmay()),
                id="oper-oper",
            ),
        ],
    )
    def test_tensor(self, subspaces, expected):
        op = Qsymbolic(to_node(subspaces[0]))
        for s in subspaces[1:]:
            op = op & s
        assert to_qobj(op) == expected
