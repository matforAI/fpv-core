class PrioritySelector:

    def __init__(self):
        self.objects = []

    def update(self, objects):
        """
        objects = [
          {"id":1,"priority":5,"cx":120},
          {"id":2,"priority":10,"cx":300}
        ]
        """
        self.objects = objects

    def best(self):
        if not self.objects:
            return None

        return sorted(
            self.objects,
            key=lambda o: o.get("priority", 0),
            reverse=True
        )[0]
