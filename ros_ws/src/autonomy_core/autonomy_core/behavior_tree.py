class Status:
    SUCCESS = 0
    FAILURE = 1
    RUNNING = 2


class BTNode:
    def tick(self):
        raise NotImplementedError


class Condition(BTNode):
    def __init__(self, fn):
        self.fn = fn

    def tick(self):
        return Status.SUCCESS if self.fn() else Status.FAILURE


class Action(BTNode):
    def __init__(self, fn):
        self.fn = fn

    def tick(self):
        self.fn()
        return Status.RUNNING


class Sequence(BTNode):
    def __init__(self, nodes):
        self.nodes = nodes

    def tick(self):
        for n in self.nodes:
            r = n.tick()
            if r != Status.SUCCESS:
                return r
        return Status.SUCCESS


class Selector(BTNode):
    def __init__(self, nodes):
        self.nodes = nodes

    def tick(self):
        for n in self.nodes:
            r = n.tick()
            if r != Status.FAILURE:
                return r
        return Status.FAILURE
