import tkinter as tk


class Simulator:
    def __init__(self, framebuffer, scale=1):
        self.fb = framebuffer
        self.scale = scale
        self.touch_callback = None

        self.root = tk.Tk()
        self.touch_callback = None
        self.root.title("Jay-Tab Simulator")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=self.fb.width * scale,
            height=self.fb.height * scale,
            bg="white",
            highlightthickness=0
        )

        self.canvas.bind("<Button-1>", self._handle_click)

        self.canvas.pack()

        self.photo = tk.PhotoImage(
            width=self.fb.width,
            height=self.fb.height
        )

        self.canvas.create_image(
            0,
            0,
            image=self.photo,
            anchor=tk.NW
        )

    def update(self):
        pixels = []

        for y in range(self.fb.height):
            row = []

            for x in range(self.fb.width):
                if self.fb.get_pixel(x, y):
                    row.append("#000000")
                else:
                    row.append("#FFFFFF")

            pixels.append(row)

        self.photo.put(pixels)

        self.root.update_idletasks()
        self.root.update()

    def start_clock(self, callback):
        def tick():
            callback()
            self.root.after(1000, tick)

        self.root.after(1000, tick)
    def start_calendar_updates(self, callback):
        def tick():
            callback()
            self.root.after(1000, tick)
        self.root.after(1000, tick)
    def run_on_main_thread(self, callback, *args):
        self.root.after(0, callback, *args)

    def start_govee_updates(self, callback):
         def tick():
              callback()
              self.root.after(1000, tick)
         self.root.after(1000, tick)

    def run(self):
            self.root.mainloop()

    def set_touch_callback(self, callback):
        self.touch_callback = callback
        self.canvas.bind("<Button-1>", self._handle_click)

    def set_event_callback(self, callback):
         self.event_callback = callback

    def broadcast(self, event, data=None):
         if self.event_calback:
              self.event_callback(event, data)

    def _handle_click(self, event):
            x = event.x // self.scale
            y = event.y // self.scale
    
            self.touch_callback({
                "x": x,
                "y": y
            })

    def start_timer(self, callback):
         def tick():
              callback()
              self.root.after(1000, tick)

         self.root.after(1000, tick)

    def schedule(self, callback, delay):
         self.root.after(delay, callback)