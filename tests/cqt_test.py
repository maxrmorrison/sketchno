import argparse
import librosa
import numpy as np
import os
import pickle
import scipy.signal as signal
import time
from matplotlib import pyplot as plt
from cqt_toolbox.cqt import cqt
from cqt_toolbox.icqt import icqt

def main(audio_file):
    # cqt parameters
    fmin = 32.7 # C1
    fmax = 16744 # C10
    fres = 12 # bins per octave
    gamma = 10

    audio, sampling_rate = librosa.load(audio_file, sr=22050)
    audio = audio[:int(11025/4)]

    start = time.clock()

    # Compute cqts of all four signals
    Xcq1 = cqt(audio, fres, sampling_rate, fmin, fmax, gamma=gamma)
    with open('cqt_params.pkl', 'wb') as f:
        pickle.dump(Xcq1, f)
    Xcqt1 = Xcq1['cqt']
    print(Xcqt1.shape)

    # Check how long cqt computation took
    cqt_time = time.clock()

    # Take the icqt before plotting for timing purposes
    re_signal1 = icqt(Xcq1)

    # Clock the icqt time
    icqt_time = time.clock() - cqt_time

    # Write the reconstructed signals to file
    librosa.output.write_wav('reconstructed.wav', re_signal1, sampling_rate)

    # Compute reconstruction error and output times
    def norm2(x):
        return np.sqrt(np.sum(np.square(x)))

    print('Time to compute cqt in secs:',cqt_time,'\nTime to compute icqt in secs:',icqt_time,'\n')

    print('Signal reconstruction error:',20*np.log10(norm2(re_signal1-audio)/norm2(audio)))

    # Plot all 4 cqts together
    plt.pcolormesh(np.abs(Xcqt1))
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('audio_file')
    args = parser.parse_args()
    main(args.audio_file)
