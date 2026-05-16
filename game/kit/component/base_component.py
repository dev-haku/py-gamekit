class BaseComponent:
    def __init__(self):
        self.active = True
        self.is_started = False
        self.parent_gameobject = None

    def start(self, engine):
        pass

    def update(self, engine):
        pass