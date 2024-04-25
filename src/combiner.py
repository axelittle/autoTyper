from natsort import natsorted
import os

combined_file_path = "lessons.txt"
text = ""

files = os.listdir("files/")
files = natsorted(files)

i = 0

for path in files:
    i += 1
    print(f"[i] Adding {path}   {i}")
    with open("files/" + path, "r", encoding="utf-8") as file:
        text += file.read() + "\n"

with open(combined_file_path, "w", encoding="utf-8") as file:
    file.write(text)
