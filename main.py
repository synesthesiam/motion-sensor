#!/usr/bin/env python3
import time
import threading
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)

from gpiozero import MotionSensor

MOTION_PIN = 13

motion_sensor = MotionSensor(MOTION_PIN)

# -----------------------------------------------------------------------------


def main():
    sleep_display()

    for proc in [motion_thread, display_thread]:
        threading.Thread(target=proc, daemon=True).start()

    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        sleep_display()


# -----------------------------------------------------------------------------


def wake_display():
    subprocess.check_call(["xset", "dpms", "force", "on"], env={"DISPLAY": ":0"})


def sleep_display():
    subprocess.check_call(["xset", "dpms", "force", "off"], env={"DISPLAY": ":0"})


wake_time = 0


def motion_thread():
    global wake_time

    while True:
        motion_sensor.wait_for_motion()
        wake_display()
        wake_time = 2 * 60
        time.sleep(1)


def display_thread():
    global wake_time

    while True:
        time.sleep(0.1)
        if wake_time > 0:
            wake_time = wake_time - 0.1
            if wake_time <= 0:
                sleep_display()


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
