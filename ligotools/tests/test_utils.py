import numpy as np
from ligotools.utils import whiten, write_wavfile, reqshift

# Test 1
def test_whiten_same_length():
    x = np.random.randn(1000)
    # fake PSD: all ones
    interp_psd = lambda f: np.ones_like(f)
    dt = 1.0 / 4096

    y = whiten(x, interp_psd, dt)

    assert len(y) == len(x)

# Test 2
def test_reqshift_keeps_length():
    x = np.sin(2 * np.pi * 10 * np.linspace(0, 1, 4096))
    y = reqshift(x, fshift=100, sample_rate=4096)

    assert len(y) == len(x)

# Test 3
def test_write_wavfile_creates_file(tmp_path):
    fname = tmp_path / "test.wav"
    data = np.random.randn(500)
    fs = 4096

    write_wavfile(str(fname), fs, data)

    assert fname.exists()
    assert fname.stat().st_size > 0

