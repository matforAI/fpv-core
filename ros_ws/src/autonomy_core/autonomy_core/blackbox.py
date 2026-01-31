import time
import json


class BlackBox:

    def __init__(self, path="/tmp/flight.log"):
        self.file = open(path, "a")

    def log(self, event, data):
        row = {
            "time": time.time(),
            "event": event,
            "data": data
        }
        self.file.write(json.dumps(row) + "\n")
        self.file.flush()
