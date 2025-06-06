import board
import digitalio
import rotaryio

# Y-Axis encoder
y_axis_encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP16)
y_axis_encoder_button = digitalio.DigitalInOut(board.GP18)
y_axis_encoder_button.direction = digitalio.Direction.INPUT
y_axis_encoder_button.pull = digitalio.Pull.UP

# LED encoder
led_encoder = rotaryio.IncrementalEncoder(board.GP27, board.GP26)
led_encoder_button = digitalio.DigitalInOut(board.GP22)
led_encoder_button.direction = digitalio.Direction.INPUT
led_encoder_button.pull = digitalio.Pull.UP

# LEDs
led1,led2,led3,led4,led5,led6,led7,led8,led9,led10 = (
    digitalio.DigitalInOut(board.GP6),
    digitalio.DigitalInOut(board.GP7),
    digitalio.DigitalInOut(board.GP8),
    digitalio.DigitalInOut(board.GP9),
    digitalio.DigitalInOut(board.GP10),
    digitalio.DigitalInOut(board.GP11),
    digitalio.DigitalInOut(board.GP12),
    digitalio.DigitalInOut(board.GP13),
    digitalio.DigitalInOut(board.GP14),
    digitalio.DigitalInOut(board.GP15),
)

leds = [led1,led2,led3,led4,led5,led6,led7,led8,led9,led10]

for led in leds:
    led.direction = digitalio.Direction.OUTPUT

# Buttons
left_button, reverse_button, up_button, right_button = (
    digitalio.DigitalInOut(board.GP0),
    digitalio.DigitalInOut(board.GP1),
    digitalio.DigitalInOut(board.GP2),
    digitalio.DigitalInOut(board.GP3),
)

buttons = [left_button,reverse_button,right_button,up_button]

for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP