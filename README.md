# The Jay-Tab!

![The Jay-Tab!](<https://i.postimg.cc/xCQNn8pr/Screenshot-2026-09-15-at-7-58-35-AM-(1).png>)
The Jay-Tab is one of my biggest personal projects! I made it to use it as a small screen to keep on my desk!

I made this project mainly out of personal interest. As to get the money to make this project in real life, I used [Hack club's stardance program!](https://stardance.hackclub.com/)

## Features!

There are many features that are packed into Jay-Tab:

- Beautifully 3D-Printed case!
- 2-Layer PCB enclosing all the hardware!
- Running on the ESP32-S3 WROOM
- 7.5" E-Ink touchscreen display to hold all the features of the Jay-Tab!
- <b>Home screen</b> that shows all you need to know at a glimpse
- <b>Calendar screen</b> that shows all the events happening in your day!
- <b>Timer screen</b> that has a timer that you can play a timer on a dedicated screen on your desk!
- <b>Home control screen</b> that is based off the Govee API, letting you toggle your lights, and change the color!

## CAD

The CAD model is from OnShape. It is made so the screen takes up 95% of the project, along with a stem that has weights inside of it to hold the Jay-Tab.

There are multiple parts, that are all going to be held using multiple screws. The power button is on the right side stem of the project.

### Important note about the CAD!

There is a part in the CAD that is CNCed. The bottom weight is CNCed to make sure that the Jay-Tab is able to stay upright, while also giving a premium feel through weight.There is also another laser-cuttable rubber part that goes on the bottom to stop it from moving.

![The Jay-Tab!](<https://i.postimg.cc/xCQNn8pr/Screenshot-2026-09-15-at-7-58-35-AM-(1).png>)

## PCB

[![View PCB on KiCanvas](https://hack.club/pcb-badge)](https://kicanvas.org/?repo=https%3A%2F%2Fgithub.com%2FJay-Tai%2FJay-Tab%2Ftree%2Fmain%2FPCB)

The PCB is the main hub of the entire project. It is in charge of making the OLED work, running code, powering the project, and the switches. It runs based off of the ESP32-S3 WROOM.

The following image is the schematic:

<img src=https://i.postimg.cc/tRs0m09r/Screenshot-2026-09-16-at-6-00-20-PM.png alt="The schematic" width ="800"/>

And this is the PCB:
<img src=https://postimg.cc/DSvjxQxY alt="The schematic" width ="800"/>

## Firmware

The firmware for the project is based off of [python](https://www.python.org/) coding language. I made the UI Drawing Interface by myself, as I couldn't find any good libraries that are simple, and are able to support E-Ink Displays. The firmware includes the following:

- Home page that has a glimpse of your entire day with upcoming events, time, and quick controls.
- Calendar panel that is connected to your Google Calendar that shows all your events in a day
- Timer panel that allows you to create timers
- Smart home panel that connects to the Govee API, allowing you to toggle and change the color of your Govee lights.

Here is what the pages look like when connected to my APIs:

### Home Page:

<img src=https://i.postimg.cc/tRs0m09r/Screenshot-2026-09-16-at-6-00-20-PM.png alt="The schematic" width ="400"/>

### Calendar:

<img src=https://i.postimg.cc/13SkvfWB/Screenshot-2026-09-16-at-8-35-49-PM.png alt="The schematic" width ="400"/>

### Timer:

<img src=https://i.postimg.cc/YqTVh8Lf/Screenshot-2026-09-16-at-9-23-52-PM.png alt="The schematic" width ="400"/>

### Home Control:

<img src=https://i.postimg.cc/L8fWffjG/Screenshot-2026-09-16-at-9-23-59-PM.png alt="The schematic" width ="400"/>

## Quick Start

To make your own Jay-Tab, it is <b>crucial</b> that you follow these steps so that everything works with your environment!

<u>1: Create your Google Calendar API!</u>
The first step to making your own Jay-Tab is to create your own Google Calendar API. You can use the Google Cloud Calender API by clicking [here](https://console.cloud.google.com/marketplace/product/google/calendar-json.googleapis.com?q=search&referrer=search&project=jay-tab). Download the file that has your key, and rename it to <i>calendar_desktop_credentials.json</i>

<u>2: Create your Govee API!</u>
The second step is to create the Govee API! Use the [following guide](https://developer.govee.com/docs/getting-started) to create your own govee API!

Once you get the Govee API, put it in under "apikey"

<u>3: Change your home screen name!</u>
To change the name on the Home Screen, use the adobe illustrator file that is attached under the software folder of the Jay-Tab. This will let you change the name from my name (Jay) to whatever it is!

# BOM

To make your own Jay-Tab, use the BOM under /bom.csv! :D
