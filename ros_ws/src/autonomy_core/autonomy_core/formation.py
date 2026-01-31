class Formation:

    def __init__(self, offset_x, offset_y):
        self.ox = offset_x
        self.oy = offset_y

    def target(self, leader_x, leader_y):
        return (
            leader_x + self.ox,
            leader_y + self.oy
        )
