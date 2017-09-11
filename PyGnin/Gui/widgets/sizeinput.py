from .input_box import InputBox


class SizeInput(InputBox):
    _default_size = (50, 50)

    def __init__(self, surf=None, flags=None, **kwargs):
        if "size" in kwargs:
            self._default_size = kwargs["size"]
        super().__init__(surf, flags, **kwargs)
