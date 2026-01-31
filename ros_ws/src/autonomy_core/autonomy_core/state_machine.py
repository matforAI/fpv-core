from enum import Enum


class State(Enum):
    IDLE = 0
    MOVE = 1
    HOLD = 2
    FAIL = 3


class StateMachine:

    def __init__(self):
        self.state = State.IDLE

    def set_state(self, new_state):
        if new_state != self.state:
            print(f"[STATE] {self.state.name} -> {new_state.name}")
            self.state = new_state

    def update(self, has_detection, odom_ok):

        # авария
        if not odom_ok:
            self.set_state(State.FAIL)
            return self.state

        # если есть объект — стоп
        if has_detection:
            self.set_state(State.HOLD)
            return self.state

        # обычное движение
        self.set_state(State.MOVE)
        return self.state
