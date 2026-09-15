from framebuffer import FrameBuffer
from graphics import fill_screen, draw_pixel, draw_line, draw_rect, fill_rect, draw_image
from display import Display
from touch import Touch
from ui import UI
from simulator import Simulator
import govee
device_id = None
govee_is_on = False

def govee_onoff():
    global govee_is_on
    global device_id

    device_id = govee.get_device()
    state = govee.get_device_state(device_id)

    govee_is_on = state["payload"]["capabilities"][0]["state"]["value"] == 1
    print(state)

fb = FrameBuffer()
touch = Touch()
simulator = Simulator(fb)

ui = UI(
    fb,
    touch,
    simulator.update,
    simulator.run_on_main_thread,
    simulator.schedule
)

simulator.set_touch_callback(ui.handle_touch)

ui.draw()

simulator.start_clock(ui.update_clock)
simulator.start_calendar_updates(ui.update_calendar)
simulator.start_govee_updates(ui.update_state_govee)

simulator.run()