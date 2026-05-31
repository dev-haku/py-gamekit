class BaseComponent:
    def __init__(self):
        self.active: bool = True
        self._tags: list[str] = []
        self.is_started: bool = False
        self.parent_gameobject = None

    def start(self, engine):
        pass

    def update(self, engine):
        pass

    @property
    def tags(self) -> list[str]:
        return self._tags

    def add_tag(self, tag_name: str):
        self._tags.append(tag_name)