#!/bin/bash

PICO_1_MOUNT="/media/$USER/CIRCUITPY"  # Path to Pico 1 mount
PICO_2_MOUNT="/media/$USER/CIRCUITPY1"  # Path to Pico 2 mount

# Check if Pico 1 is connected
if [ -d "$PICO_1_MOUNT" ]; then
    echo "Copying Pico 1 files..."
    cp "$PICO_1_MOUNT/main.py" $HOME/mission_control/pico/pico1
    cp "$PICO_1_MOUNT/hardware_setup.py" $HOME/mission_control/pico/pico1
    cp -r "$PICO_1_MOUNT/lib/" $HOME/mission_control/pico/pico1
else
    echo "Pico 1 not found. Please check connection."
fi

# Check if Pico 2 is connected
if [ -d "$PICO_2_MOUNT" ]; then
    echo "Copying Pico 2 files..."
    cp "$PICO_2_MOUNT/main.py" $HOME/mission_control/pico/pico2
    cp "$PICO_2_MOUNT/hardware_setup.py" $HOME/mission_control/pico/pico2
    cp -r "$PICO_2_MOUNT/lib/" $HOME/mission_control/pico/pico2
else
    echo "Pico 2 not found. Please check connection."
fi

echo "Sync complete!"
