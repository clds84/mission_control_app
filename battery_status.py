import time
import board
import adafruit_max1704x
import adafruit_tca9548a

import socketio

sio = socketio.Client()

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
            print(f"[bat_gauge] Error sending battery data: {e}")
        time.sleep(1)


@sio.event
def connect():
    print("[bat_gauge] Connected to robot server")

@sio.event
def disconnect():
    print("[bat_gauge] Disconnected from robot server")

def connect_with_retry():
    while True:
        try:
            print("[bat_gauge] Attempting to connect to robot server...")
            sio.connect('http://headless4.local:8000')
            break  # If connected, exit loop
        except Exception as e:
            print(f"[bat_gauge] Connection failed: {e}")
            time.sleep(.5)

if __name__ == '__main__':
    try:
        connect_with_retry() 
        battery_life_thread()
    except KeyboardInterrupt:
        print("Mission Control stopped by user")
        sio.disconnect()
