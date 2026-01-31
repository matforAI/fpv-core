import json


class MissionLoader:

    def __init__(self, path="/tmp/mission.json"):
        self.path = path
        self.waypoints = []
        self.index = 0

    def load(self):
        try:
            with open(self.path, "r") as f:
                self.waypoints = json.load(f)
                self.index = 0
                return True
        except Exception as e:
            print("MISSION LOAD ERROR:", e)
            return False

    def has_next(self):
        return self.index < len(self.waypoints)

    def next(self):
        wp = self.waypoints[self.index]
        self.index += 1
        return wp
