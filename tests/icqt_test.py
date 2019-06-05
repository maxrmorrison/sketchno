import argparse
import cv2
import librosa
import numpy as np
import pickle
import sounddevice as sd
from audio_utilities import reconstruct_signal_griffin_lim
from matplotlib import pyplot as plt
from cqt_toolbox.icqt import icqt

def main(image_file):
    image = cv2.cvtColor(cv2.imread(image_file), cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (4643, 100))
    image = image / 255.
    image[image > 0.3] = 0.
    plt.pcolormesh(image)
    plt.show()
    print(np.max(image), np.mean(image))

    with open('cqt_params.pkl', 'rb') as f:
        Xcq = pickle.load(f)
        scale = np.mean(np.abs(Xcq['cqt']), axis=1).reshape((100, 1))
    Xcq['cqt'] = np.flipud((image * scale).astype('complex'))

    signal = icqt(Xcq)

    signal /= np.max(np.abs(signal))
    print(signal.max(), signal.min(), len(signal), signal.dtype)

    sd.play(signal, 22050)

    # Plot all 4 cqts together
    plt.pcolormesh(np.abs(Xcq['cqt'] + 0.5)*255)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file')
    args = parser.parse_args()
    main(args.image_file)
