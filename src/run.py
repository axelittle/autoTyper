# Import
import os.path
import time
import pynput


# Functions
def settings():
    global lesson_id, errors, letter_time
    lesson_id = input("Enter the id of the lesson you would like to complete: ")

    while not os.path.exists(f"files/{lesson_id}.txt"):
        print("The ID is invalid.")
        lesson_id = input("Enter the id of the lesson you would like to complete: ")

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
            user_input = input("Enter the amount of mistakes you would like to get (defaults to 0): ")
            if user_input == "":
                errors = 0
                break
            errors = abs(int(user_input))
            if errors > 30:
                print("Setting more than 30 mistakes is not allowed.")
            else:
                break
        except:
            print("Invalid input.")
    print(f"[i] The application will make {errors} mistakes.")


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

lesson_id = ""

default_speed = 20000
letter_time = 0

errors = 0

# Initialize Pause-thread
listener = pynput.keyboard.Listener(on_press=on_key_press)
controller = pynput.keyboard.Controller()
listener.start()

# Get account and lesson info

print("Welcome to auto typer (alpha)!")
settings()

print("You may pause the application by pressing the escape key and resume by pressing it once more.")

# Load lesson
with open(f"files/{lesson_id}.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("The text was loaded.")
print(text)

print("Open up the tab and start the process by pressing shift.")
get_shift_press()

time.sleep(1)

# Begin typing
controller.type(" ")

time.sleep(0.3)

for char in text:
    if not running:
        exit()
    controller.type(char)
    if errors > 0:
        controller.type("°")
        errors -= 1
    time.sleep(letter_time)
    if not running:
        print("Application is paused.")
        while not running:
            time.sleep(1)
        print("Application is resuming.")
print("The application finished typing.")
input("Press enter to exit.")
