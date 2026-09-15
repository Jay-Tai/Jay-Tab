import requests

apikey = "Insert here"

url = "https://openapi.api.govee.com/router/api/v1"

def get_device():
    devices = get_light()

    for device in devices['data']:
        if device["sku"] == "H619D":
            return device ["device"]
    return None

def get_light():
    response = requests.get(
        f"{url}/user/devices",
        headers = {
            "Govee-API-Key": apikey
        }
    )

    response.raise_for_status()
    return response.json()

def get_device_state(light):
    response = requests.post(
        f"{url}/device/state",
        headers = {
            "Govee-API-Key": apikey,
            "Content-Type": "application/json"
        },
        json = {
            "requestId": "jay-tab",
            "payload": {
                "sku": "H619D",
                "device": light
            }
        }
    )

    response.raise_for_status()
    return response.json()

def turn_on(something):
    response = requests.post(
        f"{url}/device/control",
        headers = {
            "Govee-API-Key": apikey,
            "Content-Type": "application/json"
        },
        json = {
            "requestId": "jay-tab",
            "payload": {
                "sku": "H619D",
                "device": something,
                "capability": {
                    "type": "devices.capabilities.on_off",
                    "instance": "powerSwitch",
                    "value": 1
                }
            }
        }
    )

    response.raise_for_status()
    return response.json()

def turn_off(something):
    response = requests.post(
        f"{url}/device/control",
        headers = {
            "Govee-API-Key": apikey,
            "Content-Type": "application/json"
        },
        json = {
            "requestId": "jay-tab",
            "payload": {
                "sku": "H619D",
                "device": something,
                "capability": {
                    "type": "devices.capabilities.on_off",
                    "instance": "powerSwitch",
                    "value": 0
                }
            }
        }
    )

    response.raise_for_status()
    return response.json()

def set_color(light, red, green, blue):
    rgb = (red << 16) | (green << 8) | blue

    response = requests.post(
        f"{url}/device/control",
        headers = {
            "Govee-API-Key": apikey,
            "Content-Type": "application/json"
        },
        json = {
            "requestId": "jay-tab",
            "payload": {
                "sku": "H619D",
                "device": light,
                "capability": {
                    "type": "devices.capabilities.color_setting",
                    "instance": "colorRgb",
                    "value": rgb
                }
            }
        }
    )

    response.raise_for_status()
    return response.json()

print(get_device())
print(get_light())