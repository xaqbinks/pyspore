class StateMachine:
    def __init__(self):
        self.states = {}
        self.active_state = None

    def setup_states(self, states, start_state):
        self.states = states
        self.active_state = self.states[start_state]
        self.active_state.startup({})

    def flip_state(self):
        if self.active_state.done:
            previous_state_persist = self.active_state.persist
            self.active_state.done = False
            self.active_state = self.states[self.active_state.next_state]
            self.active_state.startup(previous_state_persist)

    def update(self, dt):
        self.flip_state()
        self.active_state.update(dt)

    def get_event(self, event):
        self.active_state.get_event(event)

    def draw(self, surface):
        self.active_state.draw(surface)

    @property
    def quit(self):
        return self.active_state.quit
