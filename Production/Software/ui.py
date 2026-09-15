# All imports go here
from graphics import fill_screen, draw_pixel, draw_line, draw_rect, fill_rect, draw_image, draw_text
from assets.startup_logo_array import startuplogo
from assets.screens.home_screen import home_screen
from assets.screens.timer_setup import timer_setup
from assets.screens.timer_start import timer_start
from assets.screens.calendar_screen import calendar_screen
from assets.screens.calendar_screen_multiple import calendar_screen_multiple
from assets.calendar.next_screen import calendar_next_screen
from assets.calendar.previous_screen import calendar_previous_screen
from assets.screens.home_control import home_control
import time
from clock import get_time, format_time
from datetime import datetime, timedelta
import govee
from calendar_backend import get_upcoming_events, get_events_for_day
import govee
from fonts.pt_serif import (
    FONT_DATA as PT32_DATA,
    GLYPHS as PT32_GLYPHS
)
from fonts.pt_serif_16px import (
    FONT_DATA as PT16_DATA,
    GLYPHS as PT16_GLYPHS
)
from fonts.pt_serif_56px import (
    FONT_DATA as PT56_DATA,
    GLYPHS as PT56_GLYPHS
)
from fonts.pt_serif_25px import (
    FONT_DATA as PT25_DATA,
    GLYPHS as PT25_GLYPHS
)
import threading

class UI:

    def __init__(self, framebuffer, touch, refresh, run_on_main_thread, schedule):
        self.fb = framebuffer
        self.touch = touch
        self.refresh = refresh
        self.run_on_main_thread = run_on_main_thread
        self.schedule = schedule

        self.current_screen = "startup"
        self.current_events = []

        self.timer_seconds = 1
        self.timer_minutes = 0
        self.timer_hours = 0
        self.timer_running = False
        self.timer_paused = False
        self.calendar_screen = 1
        self.items_per_screen = []
        self.calendar_over_6 = False
        self.calendar_screens = 0
        self.next_calendar_screen = True
        self.previous_calendar_screen = False
        self.calendar_month = "0"
        self.calendar_day = "0"
        self.calendar_year = "0"
        self.calendar_date = datetime.today()
        self.govee_is_on = False
        self.device_id = govee.get_device()

    def change_calendar_day(self, amt):
        self.calendar_date = self.calendar_date + timedelta(days = amt)

        self.draw_calendar()

        self.refresh()

    def show(self, screen):
        self.current_screen = screen
        self.draw()
        self.refresh()

        if screen == "home":
            self.update_calendar()

    def draw(self):
        if self.current_screen == "startup":
            self.draw_startup()

        elif self.current_screen == "home":
            self.draw_home()

        elif self.current_screen == "calendar":
            self.draw_calendar()

        elif self.current_screen == "timer":
            self.draw_timer()

        elif self.current_screen == "home-control":
            self.draw_home_control()

        elif self.current_screen == "settings":
            self.draw_settings()

        elif self.current_screen == "timer_start":
            self.draw_timer_start()


    def refresh_screen(self):
        if self.refresh:
            self.refresh()

    def update_clock(self):
        if self.current_screen != 'home':
            return

        fill_rect(
            self.fb,
            500,
            0,
            300,
            90,
            color=0
        )

        current_time = format_time()

        draw_text(
            self.fb,
            format_time(),
            603,
            60,
            PT32_DATA,
            PT32_GLYPHS
        )

        self.refresh()

    def _apply_calendar_events(self, events):
        if events == self.current_events:
            return

        self.current_events = events

        self.draw_home()
        self.refresh()

    def _fetch_calendar(self):
        try:
            events = get_upcoming_events()

            self.run_on_main_thread(
                self._apply_calendar_events,
                events
            )

        except Exception as error:
            print("Calendar update error: ",error)

    def update_calendar(self):
        if self.current_screen !="home":
            return

        thread = threading.Thread(
            target = self._fetch_calendar,
            daemon = True
        )

        thread.start()

#        events = get_upcoming_events
#        if events != self.current_events:
#            self.current_events = events
#            self.draw_home()
#            self.refresh()

    def text_width(self, text, glyphs):
        width = 0

        for character in text:
            glyph = glyphs.get(character)

            if glyph is not None:
                width += glyph[3]
        return width

    def fit_text(self, text, max_width, glyphs):
        result = ""

        for character in text:
            test = result + character

            if self.text_width(test, glyphs) > max_width:
                return result.rstrip() + "..."

            result = test

        return result
    
    def draw_upcoming_events(self):
            max_width = 296

            for index, event in enumerate(self.current_events[:6]):
                event = self.fit_text(
                    event,
                    max_width,
                    PT16_GLYPHS
                )

                draw_text(
                    self.fb,
                    event,
                    465,
                    220 + (index * 40),
                    PT16_DATA,
                    PT16_GLYPHS
                )

    def draw_timer(self):
        fill_screen(self.fb, 0)
        draw_image(self.fb, timer_setup, 0, 0)

        self.draw_timer_values()
        self.refresh()

    def draw_timer_values(self):

                fill_rect(
                    self.fb,
                    213,
                    164,
                    155,
                    73,
                    color = 0
                )

                fill_rect(
                    self.fb,
                    380,
                    164,
                    95,
                    73,
                    color = 0
                )

                fill_rect(
                    self.fb,
                    501,
                    164,
                    267,
                    73,
                    color = 0
                )
        
                draw_text(
                    self.fb,
                    str(f"{self.timer_hours:02d}"),
                    289,
                    217,
                    PT56_DATA,
                    PT56_GLYPHS
                )

                draw_text(
                    self.fb,
                    str(f"{self.timer_minutes:02d}"),
                    395,
                    217,
                    PT56_DATA,
                    PT56_GLYPHS
                )

                draw_text(
                    self.fb,
                    str(f"{self.timer_seconds:02d}"),
                    515,
                    217,
                    PT56_DATA,
                    PT56_GLYPHS
                )

    def timer_tick(self):
        if not self.timer_running:
            return

        if self.timer_paused:
            return

        if (
            self.timer_hours == 0 and
            self.timer_minutes == 0 and
            self.timer_seconds == 0
        ):
            self.timer_running = False
            return

        if self.timer_seconds > 0:
            self.timer_seconds -= 1

        else:
            self.timer_seconds = 59

            if self.timer_minutes  > 0:
                self.timer_minutes -= 1

            else:
                self.timer_minutes = 59
                self.timer_hours -= 1

        self.draw_timer_values()
        self.refresh()

        self.schedule(self.timer_tick, 1000)

    def pause_timer(self):
        self.timer_paused = True

        self.show("timer")

    def stop_timer(self):
        self.timer_running = False
        self.timer_paused = False

        self.show("timer")

    def handle_touch(self, touch):
        x = touch["x"]
        y = touch["y"]

        print("Touched:", x, y)

    def start_timer(self):
        self.timer_running = True
        self.timer_paused = False

        self.show("timer_start")

        self.schedule(self.timer_tick, 1000)

    def update_state_govee(self):
        state = govee.get_device_state(self.device_id)

        self.govee_is_on = state["payload"]["capabilities"][0]["state"]["value"] == 1
    
    
    def draw_startup(self):

        fill_screen(self.fb, 0)

        draw_image(
            self.fb,
            startuplogo,
            282,
            211
        )

        fill_rect(
            self.fb,
            253,
            297,
            294,
            2,
            color=1
        )

        fill_rect(
            self.fb,
            547,
            297,
            2,
            11,
            color=1
        )

        fill_rect(
            self.fb,
            251,
            297,
            2,
            11,
            color=1
        )

        fill_rect(
            self.fb,
            253,
            308,
            294,
            2,
            color=1
        )

        self.refresh()

        for i in range(1, 11):
            time.sleep(1)

            fill_rect(
                self.fb,
                253,
                297,
                29*i,
                11,
                color=1
            )

            self.refresh()

        time.sleep(1.5)
        self.current_screen = "home"
        self.show("home")



    def draw_home(self):
        fill_screen(self.fb, 0)

        draw_image(
            self.fb,
            home_screen,
            0,
            0
        )

        current_time = format_time()
        print("Clock:", current_time)
        draw_text(
            self.fb,
            current_time,
            603,
            60,
            PT32_DATA,
            PT32_GLYPHS
        )

        self.draw_upcoming_events()

    def draw_calendar(self):
        fill_screen(self.fb, 0)
        draw_image(
            self.fb,
            calendar_screen,
            0,
            0
        )

        draw_image(
            self.fb,
            calendar_previous_screen,
            410,
            26
        )

        request_year = self.calendar_date.year
        request_month = f"{self.calendar_date.month:02d}"
        request_day = f"{self.calendar_date.day:02d}"

        events_for_day = get_events_for_day(
            f"{request_year}-{request_month}-{request_day}"
        )
        month = self.calendar_date.strftime("%B")
        day = self.calendar_date.day
        year = self.calendar_date.year
        

        events_for_day = get_events_for_day(f'{request_year}-{request_month}-{request_day}')

        print(f"Events for day: {events_for_day}")

        month = self.calendar_date.strftime("%B")
        day = self.calendar_date.day
        year = self.calendar_date.year

        self.calendar_month = f'{self.calendar_date.month:02d}'
        self.calendar_day = f'{self.calendar_date.day:02d}'
        self.calendar_year = self.calendar_date.year

        if month == 1:
            month = 'January'
        elif month == 2:
            month = 'February'
        elif month == 3:
            month = 'March'
        if month == 4:
            month = 'April'
        elif month == 5:
            month = 'May'
        elif month == 6:
            month = 'June'
        elif month == 7:
            month = 'July'
        elif month == 8:
            month = 'August'
        elif month == 9:
            month = 'September'
        elif month == 10:
            month = 'October'
        elif month == 11:
            month = 'November'
        elif month == 12:
            month = 'December'

        draw_text(self.fb, f'{month} {str(day)}, {str(year)}', 232, 80, PT32_DATA, PT32_GLYPHS)         
        
        if len(events_for_day) <= 6:
            self.calendar_over_6 = False
            for i in range(0, len(events_for_day)):
                box_y_offset = 50 * i
                box_y_offset += 97
                text_y_offset = 50 * i
                text_y_offset += 130
                fill_rect(self.fb, 232, box_y_offset, 405, 48, color=1)

                event_text = self.fit_text(
                    events_for_day[i],
                    375,
                    PT25_GLYPHS
                )

                draw_text(
                    self.fb,
                    event_text,
                    246,
                    text_y_offset,
                    PT25_DATA,
                    PT25_GLYPHS,
                    color=0
                )

        elif len(events_for_day) > 6:

            self.items_per_screen = []

            for i in range(0, len(events_for_day), 6):
                page = events_for_day[i:i + 6]

                while len(page) < 6:
                    page.append("")

                self.items_per_screen.append(page)

            self.calendar_screens = len(self.items_per_screen)

            fill_screen(self.fb, 0)

            draw_image(
                self.fb,
                calendar_screen_multiple,
                0,
                0
            )

            today = datetime.today()
            month = today.month
            day = today.day
            year = today.year

            if month == 1:
                month = 'January'
            elif month == 2:
                month = 'February'
            elif month == 3:
                month = 'March'
            if month == 4:
                month = 'April'
            elif month == 5:
                month = 'May'
            elif month == 6:
                month = 'June'
            elif month == 7:
                month = 'July'
            elif month == 8:
                month = 'August'
            elif month == 9:
                month = 'September'
            elif month == 10:
                month = 'October'
            elif month == 11:
                month = 'November'
            elif month == 12:
                month = 'December'

            self.calendar_over_6 = True

            print(f'{month} {str(day)}, {str(year)}')

            draw_text(
                self.fb,
                f'{month} {str(day)}, {str(year)}',
                232,
                80,
                PT32_DATA,
                PT32_GLYPHS
            )

            self.calendar_screen = 1

            for i in range(0, 6):
                fill_rect(
                    self.fb,
                    232,
                    96 + (50 * i),
                    405,
                    48,
                    color=1
                )

                event_text = self.fit_text(
                    self.items_per_screen[self.calendar_screen - 1][i],
                    375,
                    PT25_GLYPHS
                )

                draw_text(
                    self.fb,
                    event_text,
                    245,
                    130 + (50 * i),
                    PT25_DATA,
                    PT25_GLYPHS,
                    color=0
                )

            # DOWN / NEXT ARROW

            if self.calendar_screen < self.calendar_screens:
                draw_image(
                    self.fb,
                    calendar_next_screen,
                    410,
                    436
                )

            # UP / PREVIOUS ARROW

            if self.calendar_screen > 1:
                draw_image(
                    self.fb,
                    calendar_previous_screen,
                    410,
                    26
                )

    def draw_timer_start(self):
        fill_screen(self.fb, 0)

        draw_image(
            self.fb,
            timer_start,
            0,
            0
        )

        self.draw_timer_values()

        

    def draw_home_control(self):
         fill_screen(self.fb, 0)
         draw_image(self.fb, home_control, 0, 0)
         pass

    def draw_settings(self):
         fill_screen(self.fb, 0)

         pass

    def update(self):
         touch = self.touch.read()

         if touch:
              self.handle_touch(touch)

    def handle_touch(self, touch):
         x = touch["x"]
         y = touch["y"]

         print(f"Touched: {x}, {y}")

         if self.current_screen == "home":
            if x >= 90 and x <= 431 and y >= 237 and y <= 330:
                self.show("timer")

            elif x >= 12 and x <= 57 and y >= 164 and y <= 208:
                self.show("timer")

            elif x >= 87 and x <= 434 and y >= 123 and y <= 222:
                self.show("calendar")

            elif x >= 13 and x <= 59 and y >= 101 and y <= 148:
                self.show("calendar")

            elif x >= 689 and y <= 760 and y >= 148 and y <= 174:
                self.show("calendar")

            elif x >= 89 and y >= 353 and x <= 433 and y <= 449:
                self.show("home-control")

         elif self.current_screen == "timer":
             if x >= 24 and y >= 26 and x <= 48 and y <= 52:
                 self.show("home")

             elif x >= 12 and y >= 102 and x <= 57 and y <= 149:
                 self.show("calendar")

             elif x >= 9 and y >= 229 and x <= 59 and y <= 276:
                 self.show("home-control")
             elif x >= 280 and x <= 350 and y >= 131 and y <= 156: # Add 1 hour to timer
                 if self.timer_hours < 9:
                    self.timer_hours += 1
            
                    print(f"Adding 1 hour to timer... New timer hours is {self.timer_hours}")
            
                    fill_rect(
                        self.fb,
                        121,
                        164,
                        220,
                        76,
                        color = 0
                    )
            
                    draw_text(
                        self.fb,
                        str(self.timer_hours),
                        289,
                        217,
                        PT56_DATA,
                        PT56_GLYPHS
                    )

                    self.refresh()

             elif x >= 280 and x <= 326 and y >= 242 and y <= 266: #Remove 1 hour from timer
                 if self.timer_hours > 0:
                    self.timer_hours -= 1

                    print(f"Adding 1 hour to timer... New timer hours is {self.timer_hours}.")

                    fill_rect(
                        self.fb,
                        121,
                        164,
                        220,
                        76,
                        color = 0
                    )
            
                    draw_text(
                        self.fb,
                        str(self.timer_hours),
                        289,
                        217,
                        PT56_DATA,
                        PT56_GLYPHS
                    )

                    self.refresh()                    
  
             elif x >= 402 and x <= 450 and y > 131 and y <= 156:
                 if self.timer_minutes < 59:
                    self.timer_minutes += 1

                    print(f"Adding 1 minute to timer... New timer minutes is {self.timer_minutes}.")

                    if self.timer_minutes <= 9:
                        fill_rect(
                            self.fb,
                            371,
                            164,
                            105,
                            76,
                            color = 0
                        )

                        draw_text(
                            self.fb,
                            str(self.timer_minutes),
                            411,
                            217,
                            PT56_DATA,
                            PT56_GLYPHS
                                 )

                        self.refresh()

                    if self.timer_minutes >= 10:
                        fill_rect(
                            self.fb,
                            371,
                            164,
                            105,
                            76,
                            color = 0
                        )

                        draw_text(
                            self.fb,
                            str(self.timer_minutes),
                            395,
                            217,
                            PT56_DATA,
                            PT56_GLYPHS
                        )

                        self.refresh()
  
                 elif self.timer_minutes == 59:
                     self.timer_minutes = 0

                     print("Resetting timer minutes to 0")

                     fill_rect(
                        self.fb,
                            371,
                            164,
                            105,
                            76,
                            color = 0
                        )

                     draw_text(
                            self.fb,
                            str(self.timer_minutes),
                            411,
                            217,
                            PT56_DATA,
                            PT56_GLYPHS
                                 )

                     self.refresh()
  
             elif x >= 402 and x <= 450 and y >= 242 and y <= 266:
                 if self.timer_minutes == 0:
                    self.timer_minutes = 59

                    print(f"Changing timer minutes to 59")

                    fill_rect(
                        self.fb,
                            371,
                            164,
                            105,
                            76,
                            color = 0
                        )

                    draw_text(
                            self.fb,
                            str(self.timer_minutes),
                            411,
                            217,
                            PT56_DATA,
                            PT56_GLYPHS
                                 )

                    self.refresh()

                 elif self.timer_minutes <= 60:

                    self.timer_minutes -= 1 

                    print(f"Removing 1 minute from timer... New minutes is {self.timer_minutes}.")

                    fill_rect(
                        self.fb,
                            371,
                            164,
                            105,
                            76,
                            color = 0
                        )

                    draw_text(
                            self.fb,
                            str(self.timer_minutes),
                            411,
                            217,
                            PT56_DATA,
                            PT56_GLYPHS
                        )

                    self.refresh()

             elif x >= 519 and x <= 565 and y >= 131 and y <= 156:
                if self.timer_seconds == 59:
                    self.timer_seconds = 1

                    print("Resetting timer seconds to 1.")

                    fill_rect(
                        self.fb,
                        498,
                        162,
                        290,
                        69,
                        color = 0
                    )

                    draw_text(
                                 self.fb,
                                 str(self.timer_seconds),
                                 528,
                                 217,
                                 PT56_DATA,
                                 PT56_GLYPHS
                             )

                elif self.timer_seconds < 59:
                    self.timer_seconds += 1

                    fill_rect(
                        self.fb,
                        498,
                        162,
                        290,
                        69,
                        color = 0
                    )

                    if self.timer_seconds <= 9:
                        draw_text(
                            self.fb,
                            str(self.timer_seconds),
                            528,
                            217,
                            PT56_DATA,
                            PT56_GLYPHS
                        )

                    elif self.timer_seconds >= 10:
                        draw_text(
                            self.fb,
                            str(self.timer_seconds),
                            500,
                            217,
                            PT56_DATA,
                            PT56_GLYPHS
                        )

                    self.refresh()

             elif x >= 519 and x <= 565 and y >= 242 and y <= 266:
                if self.timer_seconds == 1:
                    self.timer_seconds = 59

                    fill_rect(self.fb,
                              498,
                              162,
                              290,
                              69,
                              color = 0)

                    draw_text(
                        self.fb,
                        str(self.timer_seconds),
                        515,
                        217,
                        PT56_DATA,
                        PT56_GLYPHS
                    )
                    
                elif self.timer_seconds <= 59:
                    self.timer_seconds -= 1

                    if self.timer_seconds <= 9:
                        draw_text(
                            self.fb,
                            str(self.timer_seconds),
                            528,
                            217,
                            PT56_DATA,
                            PT56_GLYPHS
                        )

                    elif self.timer_seconds >= 10:
                        draw_text(
                            self.fb,
                            str(self.timer_seconds),
                            515,
                            217,
                            PT56_DATA,
                            PT56_GLYPHS
                        )
             elif x >= 24 and x <= 50 and y >= 26 and y <= 50:
                self.show("home")

             elif x >= 272 and x <= 424 and y >= 290 and y <= 349:
                self.timer_seconds = 1
                self.timer_minutes = 0
                self.timer_hours = 0

                fill_rect(
                    self.fb,
                    213,
                    164,
                    141,
                    73,
                    color = 0
                )

                fill_rect(
                    self.fb,
                    380,
                    164,
                    95,
                    73,
                    color = 0
                )

                fill_rect(
                    self.fb,
                    501,
                    164,
                    267,
                    73,
                    color = 0
                )

                draw_text(
                    self.fb,
                    str(self.timer_hours),
                    289,
                    217,
                    PT56_DATA,
                    PT56_GLYPHS
                )

                draw_text(
                    self.fb,
                    str(self.timer_minutes),
                    411,
                    217,
                    PT56_DATA,
                    PT56_GLYPHS
                )

                draw_text(
                    self.fb,
                    str(self.timer_seconds),
                    528,
                    217,
                    PT56_DATA,
                    PT56_GLYPHS
                )

                self.refresh()
             elif x >= 430 and x <= 579 and y >= 290 and y <= 349:
                 self.start_timer()

         elif self.current_screen == "timer_start":
             if x >= 272 and x <= 424 and y >= 290 and y <= 349:
                 self.pause_timer()

             elif x >= 430 and x <= 583 and y >= 290 and y <= 349:
                 self.stop_timer()
             if x >= 24 and y >= 26 and x <= 48 and y <= 52:
                 self.show("home")
             
             elif x >= 11 and y >= 165 and x <= 57 and y <= 212:
                 self.show("timer")

             elif x >= 12 and y >= 102 and x <= 57 and y <= 149:
                 self.show("calendar")

             elif x >= 9 and y >= 229 and x <= 59 and y <= 276:
                 self.show("home-control")
         elif self.current_screen == "calendar":

            if x >= 24 and y >= 26 and x <= 48 and y <= 52:
                 self.show("home")
             
            elif x >= 11 and y >= 165 and x <= 57 and y <= 212:
                 self.show("timer")

            elif x >= 9 and y >= 229 and x <= 59 and y <= 276:
                 self.show("home-control")

            # DOWN / NEXT ARROW
            elif x >= 410 and x <= 459 and y >= 435 and y <= 457 and self.calendar_over_6:

                if self.calendar_screen < self.calendar_screens:
                    self.calendar_screen += 1

                    fill_screen(self.fb, 0)

                    draw_image(
                        self.fb,
                        calendar_screen_multiple,
                        0,
                        0
                    )

                    today = datetime.today()
                    month = today.strftime("%B")
                    day = today.day
                    year = today.year

                    draw_text(
                        self.fb,
                        f'{month} {day}, {year}',
                        232,
                        80,
                        PT32_DATA,
                        PT32_GLYPHS
                    )

                    for i in range(0, 6):

                        fill_rect(
                            self.fb,
                            232,
                            96 + (50 * i),
                            405,
                            48,
                            color=1
                        )

                        event_text = self.fit_text(
                            self.items_per_screen[self.calendar_screen - 1][i],
                            375,
                            PT25_GLYPHS
                        )

                        draw_text(
                            self.fb,
                            event_text,
                            245,
                            130 + (50 * i),
                            PT25_DATA,
                            PT25_GLYPHS,
                            color=0
                        )

                    # Show next arrow only if there is another page
                    if self.calendar_screen < self.calendar_screens:
                        draw_image(
                            self.fb,
                            calendar_next_screen,
                            410,
                            436
                        )

                    # Show previous arrow if we are past page 1
                    if self.calendar_screen > 1:
                        draw_image(
                            self.fb,
                            calendar_previous_screen,
                            410,
                            26
                        )

                    self.refresh()


            # UP / PREVIOUS ARROW
            elif x >= 410 and x <= 459 and y >= 26 and y <= 50 and self.calendar_over_6:

                if self.calendar_screen > 1:
                    self.calendar_screen -= 1

                    fill_screen(self.fb, 0)

                    draw_image(
                        self.fb,
                        calendar_screen_multiple,
                        0,
                        0
                    )

                    today = datetime.today()
                    month = today.strftime("%B")
                    day = today.day
                    year = today.year

                    draw_text(
                        self.fb,
                        f'{month} {day}, {year}',
                        232,
                        80,
                        PT32_DATA,
                        PT32_GLYPHS
                    )

                    for i in range(0, 6):

                        fill_rect(
                            self.fb,
                            232,
                            96 + (50 * i),
                            405,
                            48,
                            color=1
                        )

                        event_text = self.fit_text(
                            self.items_per_screen[self.calendar_screen - 1][i],
                            375,
                            PT25_GLYPHS
                        )

                        draw_text(
                            self.fb,
                            event_text,
                            245,
                            130 + (50 * i),
                            PT25_DATA,
                            PT25_GLYPHS,
                            color=0
                        )

                    # Show next arrow if there is another page
                    if self.calendar_screen < self.calendar_screens:
                        draw_image(
                            self.fb,
                            calendar_next_screen,
                            410,
                            436
                        )

                    # Show previous arrow only if we are past page 1
                    if self.calendar_screen > 1:
                        draw_image(
                            self.fb,
                            calendar_previous_screen,
                            410,
                            26
                        )

                    self.refresh()

            elif x >= 741 and y >= 217 and x <= 766 and y <= 264:
                self.change_calendar_day(1)

            elif x >= 101 and x <= 126 and y >= 217 and y <= 264:
                self.change_calendar_day(-1)
         elif self.current_screen == "home-control":

             if x >= 24 and y >= 26 and x <= 48 and y <= 52:
                 self.show("home")
             
             elif x >= 11 and y >= 165 and x <= 57 and y <= 212:
                 self.show("timer")

             elif x >= 12 and y >= 102 and x <= 57 and y <= 149:
                 self.show("calendar")

             elif x >= 9 and y >= 229 and x <= 59 and y <= 276:
                 self.show("home-control")

             elif x >= 185 and x <= 250 and y >= 237 and y <= 400:
                 if self.govee_is_on:
                     govee.turn_off(self.device_id)
                     self.govee_is_on = False
                 else:
                     govee.turn_on(self.device_id)
                     self.govee_is_on = True
             elif x >= 483 and x <= 625 and y >= 142 and y <= 189:
                 govee.set_color(self.device_id, 255, 255, 255)
             elif x >= 332 and y >= 203 and x <= 475 and y <= 250:
                 govee.set_color(self.device_id, 0, 0, 255)
             elif x >= 483 and y >= 203 and x <= 625 and y <= 250:
                 govee.set_color(self.device_id, 0, 128, 0)
             elif x >= 633 and y >= 203 and x <= 776 and y <= 250:
                 govee.set_color(self.device_id, 255, 234, 0)
             elif x >= 332 and y >= 264 and x <= 475 and y <= 310:
                 govee.set_color(self.device_id, 255, 0, 0)
             elif x >= 483 and y >= 264 and x <= 625 and y <= 310:
                 govee.set_color(self.device_id, 255, 141, 162)
             elif x >= 633 and y >= 264 and x <= 776 and y <= 310:
                 govee.set_color(self.device_id, 108, 117, 125)
             elif x >= 332 and y >= 335 and x <= 475 and y <= 371:
                 govee.set_color(self.device_id, 232, 93, 4)
             elif x >= 483 and y >= 335 and x <= 625 and y <= 371:
                 govee.set_color(self.device_id, 144, 212, 255)
             elif x >= 633 and y >= 335 and x <= 776 and y <= 371:
                 govee.set_color(self.device_id, 108, 59, 170)