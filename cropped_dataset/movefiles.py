import os
import shutil

# Need to swap names of training and validation folders after transferring everything

folder = "velodyne"
filetype = ".bin"

with open("ImageSets/val.txt", "r") as f:
    for line in f:
        file = line.strip("\n")
        file = int(file)
        shutil.move(f"real_training/{folder}/{file}{filetype}", f"validation/{folder}/{file}{filetype}")

print("----END----")        