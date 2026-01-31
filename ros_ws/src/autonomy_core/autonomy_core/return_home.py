class ReturnHome:

    def __init__(self):
        self.home = None

    def update_home(self, odom):
        if self.home is None:
            self.home = (
                odom.pose.pose.position.x,
                odom.pose.pose.position.y
            )

    def get_home(self):
        return self.home
