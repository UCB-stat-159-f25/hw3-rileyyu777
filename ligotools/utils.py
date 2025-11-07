import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

# Function: whiten
def whiten(strain, interp_psd, dt):
    """
    Whiten the strain data using an interpolated power spectral density (PSD).

    Parameters
    ----------
    strain : numpy.ndarray
        The input time-series strain data.
    interp_psd : function
        Interpolated PSD function from scipy.interpolate.interp1d.
    dt : float
        Sampling interval in seconds.
    """
    Nt = len(strain)
    freqs = np.fft.rfftfreq(Nt, dt)

    # whitening: transform to freq domain, divide by ASD, then transform back
    hf = np.fft.rfft(strain)
    norm = 1.0 / np.sqrt(1.0 / (dt * 2))
    white_hf = hf / (np.sqrt(interp_psd(freqs)) * norm)
    white_ht = np.fft.irfft(white_hf, n=Nt)
    return white_ht


# Function: write_wavfile
def write_wavfile(filename, fs, data):
    d = np.int16(data / np.max(np.abs(data)) * 32767 * 0.9)
    wavfile.write(filename, int(fs), d)


# Function: reqshift
def reqshift(data, fshift=100.0, sample_rate=4096):
    x = np.fft.rfft(data)
    T = len(data) / float(sample_rate)
    df = 1.0 / T
    nbins = int(fshift / df)
    # print T,df,nbins,x.real.shape
    y = np.roll(x.real, nbins) + 1j * np.roll(x.imag, nbins)
    y[0:nbins] = 0.0
    z = np.fft.irfft(y)
    return z

# Function: plot_match_resulte
def plot_match_results(
    det,
    time,
    timemax,
    SNR,
    pcolor,
    strain_whitenbp,
    template_match,
    tevent,
    datafreq,
    template_fft,
    d_eff,
    freqs,
    data_psd,
    eventname,
    plottype,
):
    """
    Plot the matched filter results for a detector.
    Creates three figures:
      1. SNR vs time
      2. whitened strain + template
      3. ASD (Amplitude Spectral Density) + template FFT
    """
    # 1. SNR plots
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(time - timemax, SNR, pcolor, label=det + ' SNR(t)')
    plt.grid(True)
    plt.ylabel('SNR')
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.legend(loc='upper left')
    plt.title(det + ' matched filter SNR around event')

    plt.subplot(2, 1, 2)
    plt.plot(time - timemax, SNR, pcolor, label=det + ' SNR(t)')
    plt.grid(True)
    plt.ylabel('SNR')
    plt.xlim([-0.15, 0.05])
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.legend(loc='upper left')
    plt.savefig(f'figures/{eventname}_{det}_SNR.{plottype}')

    # 2. whitened strain and residuals
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(time - tevent, strain_whitenbp, pcolor, label=det + ' whitened h(t)')
    plt.plot(time - tevent, template_match, 'k', label='Template(t)')
    plt.ylim([-10, 10])
    plt.xlim([-0.15, 0.05])
    plt.grid(True)
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.ylabel('whitened strain (units of noise stdev)')
    plt.legend(loc='upper left')
    plt.title(det + ' whitened data around event')

    plt.subplot(2, 1, 2)
    plt.plot(time - tevent, strain_whitenbp - template_match, pcolor, label=det + ' resid')
    plt.ylim([-10, 10])
    plt.xlim([-0.15, 0.05])
    plt.grid(True)
    plt.xlabel(f'Time since {timemax:.4f}')
    plt.ylabel('whitened strain (units of noise stdev)')
    plt.legend(loc='upper left')
    plt.title(det + ' Residual whitened data after subtracting template around event')
    plt.savefig(f'figures/{eventname}_{det}_matchtime.{plottype}')

    # 3. ASD (freq domain)
    plt.figure(figsize=(10, 6))
    template_f = np.abs(template_fft) * np.sqrt(np.abs(datafreq)) / d_eff
    plt.loglog(datafreq, template_f, 'k', label='template(f)*sqrt(f)')
    plt.loglog(freqs, np.sqrt(data_psd), pcolor, label=det + ' ASD')
    plt.xlim(20, max(20, datafreq.max()))
    plt.ylim(1e-24, 1e-20)
    plt.grid(True)
    plt.xlabel('frequency (Hz)')
    plt.ylabel('strain noise ASD (strain/rtHz), template h(f)*rt(f)')
    plt.legend(loc='upper left')
    plt.title(det + ' ASD and template around event')
    plt.savefig(f'figures/{eventname}_{det}_matchfreq.{plottype}')