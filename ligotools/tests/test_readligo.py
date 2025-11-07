import numpy as np
from ligotools import readligo

# Test 1
def test_loaddata_h1_shapes_match():
    strain, time, meta = readligo.loaddata(
        "data/H-H1_LOSC_4_V2-1126259446-32.hdf5",
        'H1'
    )
    assert len(strain) == len(time)

# Test 2
def test_loaddata_time_monotonic():
    strain, time, meta = readligo.loaddata(
        "data/H-H1_LOSC_4_V2-1126259446-32.hdf5",
        'H1'
    )
    diffs = np.diff(time)
    assert (diffs >= 0).all()
    