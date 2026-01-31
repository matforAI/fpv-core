import time


class FailSafe:

    def __init__(self):
        self.last_odom_time = time.time()
        self.last_detection_time = time.time()

        self.odom_timeout = 0.5
        self.detection_timeout = 1.0

    def update_odom(self):
        self.last_odom_time = time.time()

    def update_detection(self):
        self.last_detection_time = time.time()

    def odom_ok(self):
        return (time.time() - self.last_odom_time) < self.odom_timeout

    def detection_alive(self):
        return (time.time() - self.last_detection_time) < self.detection_timeout
