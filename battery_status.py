import time
import board
import serial
import socketio
import logging
import sys
import adafruit_max1704x
import adafruit_tca9548a

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    stream=sys.stderr,  # systemd picks up stderr well
    force=True
)

# Adjust the serial port path as per your system
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
sio = socketio.Client()
sio_neo = socketio.Client()

i2c = board.I2C()

pca = adafruit_tca9548a.TCA9548A(i2c)

displayBat = adafruit_max1704x.MAX17048(pca[2])
piBat = adafruit_max1704x.MAX17048(pca[3])

def get_battery_life():
    if piBat.cell_percent > 50:
        pi_font_color = 'neon'
    elif 20 < piBat.cell_percent < 50:
        pi_font_color = 'yellow'
    else: 
        pi_font_color = 'red'

    if displayBat.cell_percent > 50:
        display_font_color = 'neon'
    elif 20 < displayBat.cell_percent < 50:
        display_font_color = 'yellow'
    else: 
        display_font_color = 'red'

    return {
        "battery": (
            "<span class='amber'>MISSION CONTROL </span> "
            "PI "
            f"<span class='{pi_font_color}'>{piBat.cell_percent:.1f}%</span> / "
            f"<span class='{pi_font_color}'>{piBat.cell_voltage:.2f}V</span> "
            "DISPLAY "
            f"<span class='{display_font_color}'>{displayBat.cell_percent:.1f}%</span> / "
            f"<span class='{display_font_color}'>{displayBat.cell_voltage:.2f}V</span>"
        )
    }
def battery_life_thread():
    while True:
        try:
            if sio.connected:
                battery_life = get_battery_life()
                sio.emit('battery_update_mc', battery_life)
        except Exception as e:
            # logging.info("[bat_gauge] Error sending battery data: {e}")
        time.sleep(1)

def read_serial_forever():
    # logging.info("[bat_gauge] Serial read thread started")
    while True:
        try:
            if sio_neo.connected:
                raw = ser.readline()
                # logging.info(f"Raw bytes: {raw}")
                line = raw.decode().strip()
                # logging.info(f"Decoded line: '{line}'")

                if line.startswith("led_encoder_button_state:"):
                    led_encoder_button_state = line.split(":")[1].split(",")[0].strip()
                    logging.info(f"Encoder state received: {led_encoder_button_state}")
                    sio_neo.emit('led_encoder_button_state', led_encoder_button_state)
        except Exception as e:
            # logging.info("[bat_gauge] Error reading serial: {e}")
        time.sleep(0.1)

@sio.event
def connect():
    # logging.info("[bat_gauge] Connected to robot server")
@sio_neo.event
def connect():
    # logging.info("Mission Control Connected to NeoPixel server")

@sio.event
def disconnect():
    # logging.info("[bat_gauge] Disconnected from robot server")
@sio_neo.event
def disconnect():
    # logging.info("Missoin Control Disconnected from NeoPixel server")


def connect_to_robot_with_retry():
    while True:
        try:
            # logging.info("[bat_gauge] Attempting to connect to robot server...")
            sio.connect('http://headless4.local:8000')
            break  # If connected, exit loop
        except Exception as e:
            # logging.info("Connection failed: {e}")
            time.sleep(.5)

def connect_to_NeoPixel_with_retry():
    while True:
        try:
            # logging.info("Mission Control Attempting to connect to NeoPixel server...")
            sio_neo.connect('http://headless4.local:9000')
            break  # If connected, exit loop
        except Exception as e:
            # logging.info("Connection failed: {e}")
            # time.sleep(.5)

if __name__ == '__main__':
    try:
        import threading
        # Start serial reading in a separate thread
        serial_thread = threading.Thread(target=read_serial_forever, daemon=True)
        serial_thread.start()
        connect_to_robot_with_retry() 
        connect_to_NeoPixel_with_retry() 
        battery_life_thread()
    except KeyboardInterrupt:
        # logging.info("Mission Control stopped by user")
        sio.disconnect()
        sio_neo.disconnect()