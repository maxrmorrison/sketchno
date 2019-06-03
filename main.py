import cv2
import numpy as np
import sounddevice as sd
import threading
import time
from sketchno import FrameRate, invert_image, Webcam

image = None
processed = None
signal = None

buffer_event = threading.Event()
img_lock = threading.Lock()
proc_lock = threading.Lock()
sig_lock = threading.Lock()


def sketch(x):
    global image
    with img_lock:
        image = x
    with proc_lock:
        return processed if processed is not None else image


def to_dac(outdata, frames, time, status):
    global signal
    with sig_lock:
        outdata[:] = signal


def start_dac():
    fps = FrameRate()
    try:
        stream = sd.OutputStream(
            samplerate=22050,
            channels=1,
            blocksize=88200*2,
            callback=to_dac,
            finished_callback=buffer_event.set)

        with stream:
            fps.step()
            key = cv2.waitKey(50)
            if key == 27:
                return
            buffer_event.wait()
    except KeyboardInterrupt:
        pass


def start_processor():
    global image
    global processed
    global signal
    while True:
        key = cv2.waitKey(50)
        if key == 27:
            break
        time.sleep(1)
        with img_lock:
            img = image
        if img is not None:
            proc, sig = invert_image(np.flipud(img))
            proc = np.flipud(cv2.resize(proc, (img.shape[1], img.shape[0])))
            with proc_lock:
                processed = proc

            sig[:200] = np.linspace(0., sig[200], num=200)
            sig[-200:] = np.linspace(sig[-200], 0., num=200)
            with sig_lock:
                signal = sig


def start_webcam():
    Webcam('Sketchno', verbose=True).start(sketch)


if __name__ == '__main__':
    t1 = threading.Thread(target=start_webcam)
    t2 = threading.Thread(target=start_dac)
    t3 = threading.Thread(target=start_processor)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
