class AntiCollision:

    def __init__(self, min_dist=1.5):
        self.min_dist = min_dist
        self.closest = 999

    def update_distance(self, distance):
        self.closest = distance

    def danger(self):
        return self.closest < self.min_dist
