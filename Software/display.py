import time

class Display:
    WIDTH = 800
    HEIGHT = 480

    def __init__(self, dc, rst, busy, spi=None, cs=None):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy

    def _command(self, command):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytes([command]))
        self.cs.value(1)

    def _data(self, data):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)

    def _reset(self):
        self.rst.value(0)
        time.sleep_ms(10)
        self.rst.value(1)
        time.sleep_ms(10)

    def _wait_until_ready(self):
        while self.busy.value():
            time.sleep_ms(10)