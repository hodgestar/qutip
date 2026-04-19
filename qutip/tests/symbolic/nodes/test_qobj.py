"""
Tests for qutip.symbolic.nodes.qobj.
"""

import qutip
from qutip.symbolic.nodes import qobj


def test_qobj_node():
    op = qutip.sigmax()
    node = qobj.from_qobj(op)

    assert node.stype == "qobj"
    assert node.dims is op._dims
    assert node.args.data is op.data
    assert node.args.isherm == op._isherm
    assert node.args.isunitary == op._isunitary
    assert node.metadata is None
