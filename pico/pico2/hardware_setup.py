import board
import digitalio
import rotaryio

# X-Axis encoder
x_axis_encoder = rotaryio.IncrementalEncoder(board.GP27, board.GP26)
x_axis_encoder_button = digitalio.DigitalInOut(board.GP28)
x_axis_encoder_button.direction = digitalio.Direction.INPUT
x_axis_encoder_button.pull = digitalio.Pull.UP

# LED encoder

led_encoder = rotaryio.IncrementalEncoder(board.GP19, board.GP20)
led_encoder_button = digitalio.DigitalInOut(board.GP21)
led_encoder_button.direction = digitalio.Direction.INPUT
led_encoder_button.pull = digitalio.Pull.UP

# LEDs 
led1,led2,led3,led4,led5,led6,led7,led8,led9,led10 = (
    digitalio.DigitalInOut(board.GP9),
    digitalio.DigitalInOut(board.GP8),
    digitalio.DigitalInOut(board.GP7),
    digitalio.DigitalInOut(board.GP6),
    digitalio.DigitalInOut(board.GP5),
    digitalio.DigitalInOut(board.GP4),
    digitalio.DigitalInOut(board.GP3),
    digitalio.DigitalInOut(board.GP2),
    digitalio.DigitalInOut(board.GP1),
    digitalio.DigitalInOut(board.GP0),
)

leds = [led1,led2,led3,led4,led5,led6,led7,led8,led9,led10]

for led in leds:
    led.direction = digitalio.Direction.OUTPUT