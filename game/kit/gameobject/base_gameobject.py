import time
from game.kit.component.destory import Destroy

class BaseGameobject:
    def __init__(self):
        self.active = True
        self.is_started = False
        self.tags: list = []
        self.components: list = []
        
        self.created_timestamp = time.time()

        self.add_component(Destroy())

    def destroy(self):
        self.get_component("Destroy").do_destroy = True

    def add_component(self, component):
        component.parent_gameobject = self
        self.components.append(component)
        return component

    def get_component(self, component_name:str):
        for component in self.components:
            if component.__class__.__name__ == component_name:
                return component
            
        return None


    def remove_component(self):
        pass
            