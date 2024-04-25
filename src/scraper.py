import time
import pynput
import pyautogui
import pyperclip


def on_click(x, y, button, pressed):
    global pos

    if button != pynput.mouse.Button.left or not pressed:
        return

    pos = (x, y)
    return False


def on_esc_press(key):
    global running
    if key == pynput.keyboard.Key.esc:
        running = False
        print("[i] Exiting.")
        exit(0)


def on_shift_press(key):
    if key == pynput.keyboard.Key.shift:
        return False


def get_click():
    with pynput.mouse.Listener(on_click=on_click) as listener:
        listener.join()
    return pos


def get_shift_press():
    with pynput.keyboard.Listener(on_press=on_shift_press) as listener:
        listener.join()


def click(pos_):
    pyautogui.click(pos_)


def write(txt):
    for char in txt:
        if char in "ÖÄÜ":
            controller.press(pynput.keyboard.Key.shift)
        controller.type(char)
        controller.release(pynput.keyboard.Key.shift)


listener = pynput.keyboard.Listener(on_press=on_esc_press)
controller = pynput.keyboard.Controller()
listener.start()
print("[i] Exit thread initialized.")

pos = ()

next_letter_pos = ()
next_letters_pos = ()
return_pos = ()

running = True
lesson = int(input("[?] Enter the lesson id: "))

character_count = int(input("[?] Character amount: "))
print(f"[i] Typing {character_count} characters.")

print("[?] Press shift to begin.")
get_shift_press()

print("[?] Click on the next letter.")
next_letter_pos = get_click()

print("[?] Click on the next letters.")
next_letters_pos = get_click()

print("[?] Click on the return position.")
return_pos = get_click()


timer = 0.3

next_letters = ""
text = ""
file_path = "file.txt"

file_path = "files/" + str(lesson) + ".txt"

print(f"[i] Application will write to \"{file_path}\".")

print("[?] Press shift to start.")
get_shift_press()

while running and len(text) <= character_count:
    click(next_letter_pos)
    click(next_letter_pos)

    pyautogui.hotkey("ctrl", "c")

    time.sleep(timer)

    click(return_pos)

    next_letters = pyperclip.paste().replace("&nbsp;", " ")[0]

    click(next_letters_pos)
    click(next_letters_pos)

    pyautogui.hotkey("ctrl", "c")

    time.sleep(timer)

    click(return_pos)

    next_letters += pyperclip.paste().replace("&nbsp;", " ")[:100]

    text += next_letters

    time.sleep(0.6)
    write(next_letters)
    time.sleep(timer)

if not running:
    exit(0)

with open(file_path, "w", encoding="utf-8") as file:
    file.write(text[:character_count])

print("[i] The file was written.\n")
