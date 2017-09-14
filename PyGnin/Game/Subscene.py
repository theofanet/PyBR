class SubScene(object):
    def __init__(self):
        super().__init__()
        self._scene = None

    def initiate(self, scene, **kargs):
        self._scene = scene
        self._initiate_data(**kargs)

    def _initiate_data(self, **kargs): pass

    def draw(self, camera=None, screen=None): pass

    def update(self): return True

    def activate(self): pass

    def close(self): pass
