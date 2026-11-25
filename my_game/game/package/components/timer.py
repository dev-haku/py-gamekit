from ..core.component import Component


class Timer(Component):
    def __init__(self, context):
        super().__init__(context)
        self._timers = []

        self.dt = self.engine.delta_time
        
    def add_timer(self, callback_method, duration_sec):
        self._timers.append({
            "elapsed": 0,
            "duration_sec": duration_sec,
            "callback_method": callback_method,
        })

    def update(self):
        for timer in self._timers:
            
            timer["elapsed"] += self.dt
            while timer["elapsed"] >= timer["duration_sec"]:
                timer["callback_method"]()
                timer["elapsed"] -= timer["duration_sec"]

        return super().update()