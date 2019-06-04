import cv2
import numpy as np
import pickle
from cqt_toolbox.icqt import icqt
from cqt_toolbox.gen_inv_filterbank import gen_inv_filterbank


def invert_image(image, threshold=0.35):
    if not hasattr(invert_image, 'cqt'):
        with open('cqt_params.pkl', 'rb') as f:
            invert_image.cqt = pickle.load(f)
            invert_image.filters = gen_inv_filterbank(
                invert_image.cqt['filter_bank'],
                invert_image.cqt['shift'],
                invert_image.cqt['bw_bins'])
            invert_image.scale = np.mean(
                np.abs(invert_image.cqt['cqt']), axis=1).reshape((100, 1))

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (580, 100))
    image = image / 255.
    image[image > threshold] = 0.
    image[:75, :] *= 2
    image[:50, :] *= 2

    invert_image.cqt['cqt'] = (image * invert_image.scale).astype('complex')

    signal = icqt(invert_image.cqt, invert_image.filters)
    signal -= signal.mean()
    signal /= np.max(np.abs(signal))

    return image, signal
