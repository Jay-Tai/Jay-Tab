class FrameBuffer:
    WIDTH = 800
    HEIGHT = 480

    def __init__(self):
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.stride = (self.width + 7) // 8
        self.buffer = bytearray(self.stride * self.height)

    def clear(self, color=0):
        value = 0xFF if color else 0x00
        self.buffer[:] = bytes([value]) * len(self.buffer)

    def pixel(self, x, y, color=1):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return

        index = y * self.stride + (x >> 3)
        mask = 0x80 >> (x & 7)

        if color:
            self.buffer[index] |= mask
        else:
            self.buffer[index] &= ~mask

    def get_pixel(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return 0

        index = y * self.stride + (x >> 3)
        mask = 0x80 >> (x & 7)

        return 1 if self.buffer[index] & mask else 0