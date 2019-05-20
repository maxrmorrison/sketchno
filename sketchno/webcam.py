import cv2
from sketchno import FrameRate

class Webcam:

    def __init__(self, window_name, device=0, wait_time=50, close_key=27, verbose=False):
        self.window_name = window_name
        self.device = device
        self.wait_time = wait_time
        self.close_key = close_key
        self.verbose = verbose
        self.frame_rate = FrameRate(interval=2)

    def start(self, callback=lambda x: x):
        # Setup
        cv2.namedWindow(self.window_name)
        cv2.namedWindow("Processed")
        camera = cv2.VideoCapture(self.device)

        if camera.isOpened():
            rval, frame = camera.read()
        else:
            rval = False

        # Loop over frames
        while rval:
            if self.verbose:
                self.frame_rate.step()
            cv2.imshow(self.window_name, frame)
            rval, frame = camera.read()
            processed = callback(frame)
            cv2.imshow("Processed", processed)
            key = cv2.waitKey(self.wait_time)
            if key == self.close_key:
                break

        # Cleanup
        camera.release()
        cv2.destroyAllWindows()

