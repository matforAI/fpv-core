#!/usr/bin/env python3

class TargetTracker:

    def __init__(self, image_width=640):
        self.image_width = image_width
        self.target_x = None

    def update_bbox(self, center_x):
        self.target_x = center_x

    def get_yaw_error(self):
        if self.target_x is None:
            return 0.0

        center = self.image_width / 2.0
        error = (self.target_x - center) / center
        return float(error)
