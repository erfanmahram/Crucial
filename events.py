from collections import defaultdict


class Event:
    def __init__(self):
        self.events = defaultdict(dict)

    def call(self, func_name, id, *args, **kwargs):
        if func_name in self.events and id in self.events[func_name]:
            return self.events[func_name][id](*args, **kwargs)
        else:
            raise ReferenceError(f"id: {id} , func name: {func_name}")

    def register(self, func_name, key, call_back):
        self.events[func_name][key] = call_back
