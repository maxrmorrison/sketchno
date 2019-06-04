import argparse
import librosa
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from cqt_toolbox.cqt import cqt

def main(audio_file):
    # cqt parameters
    fmin = 32.7 # C1
    fmax = 16744 # C10
    fres = 12 # bins per octave
    gamma = 10

    audio, sampling_rate = librosa.load(audio_file, sr=22050)

    Xcq1 = cqt(audio, fres, sampling_rate, fmin, fmax, gamma=gamma)
    Xcqt1 = Xcq1['cqt']

    # Plot all 4 cqts together
    plt.pcolormesh(np.abs(Xcqt1), cmap=cm.gray_r)
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('audio_file')
    args = parser.parse_args()
    main(args.audio_file)
