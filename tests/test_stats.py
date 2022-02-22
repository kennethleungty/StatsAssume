import os
import sys

sys.path.insert(0, os.path.abspath(".."))

from pyassume.datasets import load_data




def test_stat_breuschpagan():
    var1 = 1
    var2 = 2
    var3 = 3

    assert (var1 + var2) == var3

# def test_stat_durbin()
