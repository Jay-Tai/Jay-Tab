class Touch:
    def __init__(self, i2c = None, interrupt = None, reset = None):
        self.i2c = i2c
        self.interrupt = interrupt
        self.reset = reset
        self.touch_callback = None

    def init(self):
        pass

    def touched(self):
        return False

    def read(self):
        return None

    def _handle_click(self, event):
        x = event.x // self.scale
        y = event.y // self.scale

        self.touch_callback({
            "x": x,
            "y": y
        })

    def set_touch_callback(self, callback):
        self.touch_callback = callback
        self.canvas.bind("<Button-1>", self._handle_click)