import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from hardware_setup import (
    y_axis_encoder, y_axis_encoder_button,
    led_encoder, led_encoder_button,
    leds,left_button,reverse_button,
    right_button, up_button
)

keyboard = Keyboard(usb_hid.devices)

led_encoder_last_position = 0
led_encoder_button_state = None

y_axis_encoder_last_position = 0  

while True:
    if not y_axis_encoder_button.value:
        keyboard.press(Keycode.N)
        time.sleep(.5)
        keyboard.release(Keycode.N)
    # Clamp encoder hardware to avoid phantom steps
    if y_axis_encoder.position < 0:
        y_axis_encoder.position = 0
    elif y_axis_encoder.position > 9:
        y_axis_encoder.position = 9
    current_position = y_axis_encoder.position
    delta = current_position - y_axis_encoder_last_position

    if delta != 0:
        if delta > 0:
            for _ in range(delta):
                keyboard.press(Keycode.K)
                keyboard.release(Keycode.K)
        elif delta < 0:
            for _ in range(-delta):
                keyboard.press(Keycode.I)
                keyboard.release(Keycode.I)

        # Only update after handling steps
        y_axis_encoder_last_position = current_position

    time.sleep(0.01)

# LED logic
    position = led_encoder.position
    #Clamp position and reset hardware encoder if out of range
    if position < 0:
        position = 0
        led_encoder.position = 0
    elif position > 9:
        position = 9
        led_encoder.position = 9
        
    # Handle button toggle logic
    if not led_encoder_button.value and led_encoder_button_state is None:
        keyboard.press(Keycode.F)
        time.sleep(0.5)
        keyboard.release(Keycode.F)
        led_encoder_button_state = "pressed"
        led_encoder.position = 0
        led_encoder_last_position = 0
        for led in leds:
            led.value = True  # Turn all LEDs ON
            
    elif not led_encoder_button.value and led_encoder_button_state == "pressed":
        keyboard.press(Keycode.F)
        time.sleep(0.5)
        keyboard.release(Keycode.F)
        led_encoder_button_state = None
        led_encoder.position = 0
        led_encoder_last_position = 0
        for led in leds:
            led.value = False  # Turn all LEDs OFF

    #Handle LED rotary position to control LED bar level (if toggled on)
    if led_encoder_button_state == "pressed":
        position = led_encoder.position
        if position != led_encoder_last_position:
            delta = position - led_encoder_last_position
            position = max(0, min(9, position))  # Clamp between 0 and 9
            led_encoder_last_position = max(0, min(9, led_encoder_last_position))  # Clamp too

            if delta > 0:
                for _ in range(delta):
                    keyboard.press(Keycode.H)
                    keyboard.release(Keycode.H)
            else:
                for _ in range(-delta):
                    keyboard.press(Keycode.G)
                    keyboard.release(Keycode.G)
            for i, led in enumerate(leds):
                led.value = i  >= position
            led_encoder_last_position = position

    time.sleep(0.01)

# A-S-D-W movement (left-reverse-right-up)
    buttons_keys = [
        (left_button, Keycode.A),
        (reverse_button, Keycode.S),
        (right_button, Keycode.D),
        (up_button, Keycode.W),
    ]

    for button, key in buttons_keys:
        if not button.value:
            keyboard.press(key)
        else:
            keyboard.release(key)