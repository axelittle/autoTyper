# Import
import os.path
import random
import time
import pynput
import pyautogui
import json


# Functions
def settings():
    global error_percentage, letter_time, lesson_amount, lesson_id, use_config, error_range, speed_range
    
    if os.path.exists(config_path):
        use_config = input("[?] A config file was found. Would you like to use it? [y/n]: ").lower() == "y"

    # Load lesson
    while True:
        try:
            lesson_id = int(input("[?] Enter the id of the lesson you would like to complete: "))
            _ = text[str(lesson_id)]
            break
        except:
            print("[!] The input is invalid.")

    while True:
        try:
            lesson_amount = input("[?] Enter the amount of lessons you would like to complete (defaults to 1): ")
            if lesson_amount == "":
                lesson_amount = 1
                break
            lesson_amount = int(lesson_amount)
            _ = text[str(lesson_id + lesson_amount - 1)]
            break
        except:
            print("[!] The input is invalid.")

    if use_config:
        try:
            with open(config_path, "r") as config_file:
                config = json.loads(config_file.read())

            name = config["name"]
            print(f"[i] Using config: \"{name}\"")

            error_max = config["error_max"]
            error_min = config["error_min"]

            speed_max = config["speed_max"]
            speed_min = config["speed_min"]

            print("[i] Press shift and then click on the continue button.")
            get_shift_press()
            if config["auto_click"]:
                get_click()

            print(f"[i] Mistake range loaded as ({error_min}:{error_max}).")
            print(f"[i] Speed range loaded as ({speed_min}:{speed_max}).")

            error_range = (error_min, error_max)
            speed_range = (speed_min, speed_max)
            return
        except:
            use_config = False
            input("[!] Could not load config properly. Press enter to continue in normal mode.")

    while True:
        try:
            user_input = input("[?] Enter the keys/10min value (defaults to 20'000): ")
            if user_input == "":
                speed = 20000
                letter_time = 600 / speed
                break
            elif user_input == "inf":
                letter_time = 0
                break
            speed = abs(int(user_input))
            letter_time = 600 / speed
            break
        except:
            print("[!] Invalid input.")

    while True:
        try:
            user_input = input("[?] Enter the amount of mistakes you would like to get in percent (defaults to 0): ")
            if user_input == "":
                error_percentage = 0
                break
            error_percentage = abs(float(user_input)) / 100
            if error_percentage > 80:
                print("[!] Setting more than 80 percent is not allowed.")
            else:
                break
        except:
            print("[!] Invalid input.")
    print(f"[i] The application will make {error_percentage * 100} percent mistakes.")


def on_click(x, y, button, pressed):
    global click_position

    if button != pynput.mouse.Button.left or not pressed:
        return

    click_position = (x, y)
    return False


def get_click():
    with pynput.mouse.Listener(on_click=on_click) as click_listener:
        click_listener.join()


def click_continue():
    pyautogui.click(click_position)


def on_key_press(symbol):
    global running
    if symbol == pynput.keyboard.Key.esc:
        running = not running


def on_shift_press(key):
    if key == pynput.keyboard.Key.shift:
        return False


def get_shift_press():
    with pynput.keyboard.Listener(on_press=on_shift_press) as shift_listener:
        shift_listener.join()


# Declarations
running = True

lesson_file = "lessons.json"
config_path = "typerconfig.json"

use_config = False
error_range = ()
speed_range = ()

default_speed = 20000
letter_time = 0

error_percentage = 0

text = ""
lesson_amount = 0
lesson_id = 1

click_position = ()

# Initialize Pause-thread
listener = pynput.keyboard.Listener(on_press=on_key_press)
controller = pynput.keyboard.Controller()
listener.start()

# Load text
try:
    with open(lesson_file, "r", encoding="utf-8") as file:
        print("[i] The text file was loaded successfully.")
except:
    print("[FE] The \"lessons.json\" file could not be found. Try downloading all files again.")
    input("[i] Press enter to quit.")

# Get account and lesson info

print("[i] Welcome to autoTyper (alpha)!")
settings()

current_lesson = lesson_id

current_text = ""

while current_lesson < lesson_id + lesson_amount:
    current_text = text[str(current_lesson)]
    if use_config:
        error_percentage = random.uniform(error_range[0], error_range[1]) / 100
        letter_time = 600 / random.uniform(speed_range[0], speed_range[1])
        print(f"[i] Selected values by configuration: ({error_percentage}, {600 * letter_time}).")
        if click_position != ():
            time.sleep(3)
            click_continue()
            print("[i] Write button was clicked.")
            time.sleep(5)
    mistakes = round(error_percentage * len(current_text))

    print("[i] You may pause the application by pressing the escape key and resume by pressing it once more.")
    print(f"[i] Now doing lesson {current_lesson} with {mistakes} mistakes..")
    print(f"[i] Confirm beginning of lesson: \"{current_text[:50]}\"")
    if click_position == () or current_lesson == lesson_id:
        print("[i] Open up the tab and start the process by pressing shift.")
        get_shift_press()

    time.sleep(1)

    # Begin typing
    controller.type("#")

    time.sleep(1)

    for char in current_text:
        if not running:
            exit()
        controller.type(char)
        if mistakes >= 1:
            controller.type("°")
            mistakes -= 1
        time.sleep(letter_time)
        if not running:
            print("Application is paused.")
            while not running:
                time.sleep(1)
            print("Application is resuming.")
    current_lesson += 1
print("The application finished typing.")
time.sleep(5)
