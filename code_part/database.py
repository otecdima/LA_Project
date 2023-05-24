import hashlib
import os
from operator import itemgetter
import numpy as np
import librosa
from scipy.ndimage import maximum_filter


def find_peaks_maximum(sample, sampling_rate):
    hop_length = 512
    n_fft = 2048
    spectrogram = np.abs(librosa.stft(sample, hop_length=hop_length, n_fft=n_fft))

    filter_size = (25, 25)
    filtered_spectrogram = maximum_filter(spectrogram, size=filter_size)

    local_maxima = (spectrogram == filtered_spectrogram)

    threshold = 1
    local_maxima = np.where(spectrogram * local_maxima >= threshold)

    time_indices = local_maxima[1] * hop_length / sampling_rate
    frequencies = librosa.fft_frequencies(sr=sampling_rate, n_fft=n_fft)[local_maxima[0]]

    xs = time_indices
    ys = frequencies

    zipped = zip(xs, ys)
    zipped = list(zipped)
    time_freq = [i for i in zipped if i[1] != 0.0]
    return time_freq


def find_peaks_maximum_song(sample, sampling_rate):
    hop_length = 512
    n_fft = 2048
    spectrogram = np.abs(librosa.stft(sample, hop_length=hop_length, n_fft=n_fft))

    filter_size = (25, 25)
    filtered_spectrogram = maximum_filter(spectrogram, size=filter_size)

    local_maxima = (spectrogram == filtered_spectrogram)

    threshold = 1
    local_maxima = np.where(spectrogram * local_maxima >= threshold)

    time_indices = local_maxima[1] * hop_length / sampling_rate
    frequencies = librosa.fft_frequencies(sr=sampling_rate, n_fft=n_fft)[local_maxima[0]]

    xs = time_indices
    ys = frequencies

    zipped = zip(xs, ys)
    zipped = list(zipped)
    time_freq = [i for i in zipped if i[1] != 0.0]
    return time_freq


def generate_hashes_song(peaks):
    idx_freq = 1
    idx_time = 0

    peaks.sort(key=itemgetter(1))

    hashes = []
    for i in range(len(peaks)):
        for j in range(1, 10):
            if (i + j) < len(peaks):
                freq1 = peaks[i][idx_freq]
                freq2 = peaks[i + j][idx_freq]
                t1 = peaks[i][idx_time]
                t2 = peaks[i + j][idx_time]
                t_delta = t2 - t1

                if 0 <= t_delta <= 200:
                    h = hashlib.sha1(f"{str(freq1)}|{str(freq2)}|{str(t_delta)}".encode('utf-8'))
                    hashes.append((h.hexdigest()[0:20], t1))
    return hashes


def create_database():
    database_of_song = {}
    for filename in os.listdir('../songs'):
        f = os.path.join('../songs', filename)
        if os.path.isfile(f) and f.endswith("mp3"):
            sample, sampling_rate = librosa.load(f)
            peaks = find_peaks_maximum_song(sample, sampling_rate)
            hashes = generate_hashes_song(peaks)
            database_of_song[f.split("../songs/")[1].split(".")[0]] = hashes
    return database_of_song
