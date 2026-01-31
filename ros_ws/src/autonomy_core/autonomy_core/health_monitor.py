import psutil
import time


class HealthMonitor:

    def __init__(self):
        self.last_tick = time.time()
        self.fps = 0.0

    def tick(self):
        now = time.time()
        dt = now - self.last_tick
        self.last_tick = now
        if dt > 0:
            self.fps = 1.0 / dt

    def get(self):
        return {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "fps": round(self.fps, 1)
        }
