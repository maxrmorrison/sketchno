import argparse
import cv2
import librosa
import numpy as np
import os
import scipy.signal as signal
import time
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from audio_utilities import reconstruct_signal_griffin_lim
from cqt_toolbox.cqt import cqt
from cqt_toolbox.icqt import icqt

def main(image_file):
    # cqt parameters
    fmin = 32.7 # C1
    fmax = 16744 # C10
    octaves = 9
    fres = 12 # bins per octave
    gamma = 10

    img = cv2.imread(image_file)
    img = np.complex(img)

    # Compute cqts of all four signals
    Xcq1 = icqt(audio, fres, sampling_rate, fmin, fmax, gamma=gamma)
    Xcqt1 = Xcq1['cqt']
    print(Xcqt1.shape)

    # Check how long cqt computation took
    cqt_time = time.clock()

    # Take the icqt before plotting for timing purposes
    re_signal1, gd = icqt(Xcq1)

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
    parser.add_argument('image_file')
    args = parser.parse_args()
    main(args.audio_file)
