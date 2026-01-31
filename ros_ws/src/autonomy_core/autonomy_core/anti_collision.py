class AntiCollision:

    def __init__(self, min_dist=1.5):
        self.min_dist = min_dist
        self.closest = 999.0

    def update_scan(self, scan):
        if not scan.ranges:
            return

        valid = [r for r in scan.ranges if r > 0.05]
        if valid:
            self.closest = min(valid)

    def danger(self):
        return self.closest < self.min_dist
