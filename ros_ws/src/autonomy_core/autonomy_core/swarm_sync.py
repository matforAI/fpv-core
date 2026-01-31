import time


class SwarmSync:

    def __init__(self, drone_id):
        self.id = drone_id
        self.peers = {}

    def pack(self, state, x=0.0, y=0.0):
        return {
            "id": self.id,
            "state": state,
            "x": x,
            "y": y,
            "time": time.time()
        }

    def update_peer(self, msg):
        peer_id = msg.get("id")
        if peer_id == self.id:
            return

        self.peers[peer_id] = msg

    def alive(self, timeout=1.5):
        now = time.time()
        return {
            k: v for k, v in self.peers.items()
            if now - v["time"] < timeout
        }
