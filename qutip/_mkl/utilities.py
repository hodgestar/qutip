# This file is part of QuTiP: Quantum Toolbox in Python.
#
#    Copyright (c) 2011 and later, Paul D. Nation.
#    All rights reserved.
#
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions are
#    met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the QuTiP: Quantum Toolbox in Python nor the names
#       of its contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################

import os
import sys
from qutip.utilities import _blas_info
import qutip.settings as qset
from ctypes import cdll


def _set_mkl():
    """
    Finds the MKL runtime library for the
    Anaconda and Intel Python distributions.

    """
    if (
        _blas_info() != 'INTEL MKL'
        or sys.platform not in ['darwin', 'win32', 'linux', 'linux2']
    ):
        return
    python_dir = os.path.dirname(sys.executable)
    if sys.platform in ['darwin', 'linux2', 'linux']:
        python_dir = os.path.dirname(python_dir)
    library = {
        'darwin': 'libmkl_rt.dylib',
        'win32': 'mkl_rt.dll',
        'linux': 'libmkl_rt.so',
        'linux2': 'libmkl_rt.so',
    }[sys.platform]

    if sys.platform in ['darwin', 'linux2', 'linux']:
        locations = [
            'lib',
            os.path.join('ext', 'lib'),
        ]
    else:
        locations = [
            os.path.join('Library', 'bin'),
            os.path.join('ext', 'lib'),
        ]

    for location in locations:
        try:
            qset.mkl_lib = cdll.LoadLibrary(
                os.path.join(python_dir, location, library)
            )
            qset.has_mkl = True
            return
        except Exception:
            pass
