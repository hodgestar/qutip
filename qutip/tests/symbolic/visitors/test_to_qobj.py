"""
Tests for qutip.symbolic.visitors.to_qobj.
"""

from qutip.symbolic import Qsymbolic
from qutip.symbolic.visitors import to_qobj


class TestToQobj:
    def test_empty(self):
        op = Qsymbolic()
        assert to_qobj(op) is None

    def test_complex_constant_real(self):
        op = Qsymbolic() + 5
        assert to_qobj(op) == 5.0

    def test_complex_constant_imag(self):
        op = Qsymbolic() + 5j
        assert to_qobj(op) == 5.0j

    def test_complex_constant_complex(self):
        op = Qsymbolic() + (1 + 5j)
        assert to_qobj(op) == 1 + 5j
