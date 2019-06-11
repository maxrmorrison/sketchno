# Sketchno
Sketchno is a framework for musical expression via drawing.
Sketchno uses a video camera to create a spectrogram from the captured image.
The resulting spectrogram is inverted to recover and play an audio signal.
While originally designed for creating a drawable interface on standard printer paper or transparency paper, Sketchno can be used to sonify any live video stream (e.g., sidewalk chalk drawings or dance performances).

## Installation
Sketchno runs on Python 3 using OpenCV and SoundDevice and requires that devices for both video input and audio output are available.
To install Sketchno, clone this repo and install the dependencies with `pip install -r requirements.txt`.
Note that you must first have Python and pip installed.
To start Sketchno, run `python main.py`.

## Player Notes
Sketchno is best played by mounting your camera to look down on a flat, backlit (or white) drawing surface.
Transparency paper and dry erase markers can also be used and layered on top of each other for more control of individual musical parts.
Any sufficiently dark region of the caputured image will be detected as a bin in the spectrogram that should contain nonzero energy.
Printed spectrograms of prerecorded music can be used as source material.
The `make_spectrogram.py` script is useful for creating new spectrograms of source material.

## Technical Notes
Sketchno synthesizes audio from a spectrogram via the inverse Constant-Q Transform (CQT) [1].
The magnitude spectrogram is extracted from the image by applying a thresholding operation to the image to remove bright pixels and then applying some simple filtering.
The spectrogram phase is arbitrarily set to zero. Future work could integrate a realtime Griffin-Lim algorithm for better phase reconstruction [2].

### Bibliography
 - [1] Brown, Judith C. "Calculation of a constant Q spectral transform." The Journal of the Acoustical Society of America 89.1 (1991): 425-434.
 - [2] Griffin, Daniel, and Jae Lim. "Signal estimation from modified short-time Fourier transform." IEEE Transactions on Acoustics, Speech, and Signal Processing 32.2 (1984): 236-243.
