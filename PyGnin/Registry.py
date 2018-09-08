class Registry(object):
    _objects = {}

    @staticmethod
    def register(key, obj):
        Registry._objects[key] = obj

    @staticmethod
    def registered(key):
        if key in Registry._objects:
            return Registry._objects[key]

    @staticmethod
    def has(key):
        return key in Registry._objects
