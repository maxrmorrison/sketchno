import cv2
import logging
import numpy as np
import queue
import sounddevice as sd
import threading
import time
from sketchno import FrameRate, invert_image, Webcam

image = None
processed = None
signal_q = queue.Queue(maxsize=2)

event = threading.Event()
img_lock = threading.Lock()
proc_lock = threading.Lock()


def sketch(x):
    global image
    with img_lock:
        image = x
    with proc_lock:
        return processed if processed is not None else image


def to_dac(outdata, frames, time, status):
    try:
        global signal_q
        outdata[:] = signal_q.get()
    except KeyboardInterrupt:
        raise sd.CallbackStop


def start_dac():
    try:
        stream = sd.OutputStream(
            samplerate=22050,
            channels=1,
            blocksize=11025,
            callback=to_dac,
            finished_callback=event.set)

        with stream:
            event.wait()
    except KeyboardInterrupt:
        event.set()


def start_processor():
    global image
    global processed
    global signal_q

    location = 0
    current_played = -4
    prev_played = -5
    while not event.is_set():

        # Get current image
        with img_lock:
            img = image

        if img is not None:
            # Get current beat
            timepoints = int(img.shape[1] / 8)
            img_slice = img[:, location * timepoints:(location + 1) * timepoints]

            # Invert image spectrogram to audio
            proc, sig = invert_image(np.flipud(img_slice))
            proc = np.flipud(cv2.resize(proc, (img_slice.shape[1], img_slice.shape[0])))

            # Display the spectrogram
            with proc_lock:
                if processed is None:
                    processed = np.zeros((proc.shape[0], proc.shape[1] * 8))

                processed[:, location * timepoints:(location + 1) * timepoints] = proc
                if current_played >= 0:
                    processed[:, current_played * timepoints:(current_played + 1) * timepoints] += 0.5
                if prev_played >= 0:
                    processed[:, prev_played * timepoints:(prev_played + 1) * timepoints] -= 0.5

            # Ramp to prevent clicks
            sig[:200] = np.linspace(0., sig[200], num=200)
            sig[-200:] = np.linspace(sig[-200], 0., num=200)

            # Post signal to DAC
            signal_q.put(sig)

            current_played = (current_played + 1) % 8 if current_played >= 0 else current_played + 1
            prev_played = (prev_played + 1) % 8 if prev_played >= 0 else prev_played + 1
            location = (location + 1) % 8


def start_webcam():
    Webcam('Sketchno', verbose=True).start(sketch)


if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    t1 = threading.Thread(target=start_webcam)
    t2 = threading.Thread(target=start_dac, daemon=True)
    t3 = threading.Thread(target=start_processor, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
