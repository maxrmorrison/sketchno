import time


class FrameRate:

    def __init__(self, interval=1.0):
        self.interval = interval
        self.start = time.time()
        self.frames = 0

    def step(self):
        self.frames += 1
        if time.time() - self.start > self.interval:
            self.print()

    def print(self):
        current_time = time.time()
        elapsed = current_time - self.start
        frame_rate = self.frames / elapsed
        print('Frame rate: {} fps'.format(frame_rate))

        self.frames = 0
        self.start = current_time
