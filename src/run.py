# Import
import time
import pynput
import json


# Functions
def settings():
    global error_percentage, letter_time, lesson_amount, lesson_id

    # Load lesson
    while True:
        try:
            lesson_id = int(input("Enter the id of the lesson you would like to complete: "))
            _ = text[str(lesson_id)]
            break
        except:
            print("[!] The input is invalid.")

    while True:
        try:
            lesson_amount = input("Enter the amount of lessons you would like to complete (defaults to 1): ")
            if lesson_amount == "":
                lesson_amount = 1
                break
            lesson_amount = int(lesson_amount)
            _ = text[str(lesson_id + lesson_amount)]
            break
        except:
            print("[!] The input is invalid.")

    while True:
        try:
            user_input = input("Enter the keys/10min value (defaults to 20'000): ")
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
            print("Invalid input.")

    while True:
        try:
            user_input = input("Enter the amount of mistakes you would like to get in percent (defaults to 0): ")
            if user_input == "":
                error_percentage = 0
                break
            error_percentage = abs(int(user_input)) / 100
            if error_percentage > 20:
                print("Setting more than 30 percent is not allowed.")
            else:
                break
        except:
            print("Invalid input.")
    print(f"[i] The application will make {error_percentage * 100} percent mistakes.")


def on_key_press(symbol):
    global running
    if symbol == pynput.keyboard.Key.esc:
        running = not running


def on_shift_press(key):
    if key == pynput.keyboard.Key.shift:
        return False


def get_shift_press():
    with pynput.keyboard.Listener(on_press=on_shift_press) as listener:
        listener.join()


# Declarations
running = True

lesson_file = "lessons.txt"

default_speed = 20000
letter_time = 0

error_percentage = 0

text = ""
lesson_amount = 0
lesson_id = 1

# Initialize Pause-thread
listener = pynput.keyboard.Listener(on_press=on_key_press)
controller = pynput.keyboard.Controller()
listener.start()

# Load text
try:
    with open("lessons.json", "r", encoding="utf-8") as file:
        text = json.loads(file.read())
        print("[i] The text file was loaded successfully.")
except:
    print("[FE] the \"lessons.json\" file could not be found. Try downloading all files again.")
    input("[i] Press enter to quit.")

# Get account and lesson info

print("[i] Welcome to autoTyper (alpha)!")
settings()

current_lesson = lesson_id

current_text = ""

while current_lesson < lesson_id + lesson_amount:
    print("[i] You may pause the application by pressing the escape key and resume by pressing it once more.")
    print(f"[i] Now doing lesson {current_lesson}.")
    current_text = text[str(current_lesson)]
    print(f"[i] Confirm beginning of lesson: \"{current_text[:50]}\"")
    print("[i] Open up the tab and start the process by pressing shift.")
    get_shift_press()

    time.sleep(1)

    # Begin typing
    controller.type(" ")

    time.sleep(1)

    mistakes = round(error_percentage * len(text))
    for char in current_text:
        if not running:
            exit()
        controller.type(char)
        if mistakes > 0:
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
input("Press enter to exit.")
