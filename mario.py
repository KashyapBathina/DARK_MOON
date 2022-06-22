# TODO
from cs50 import get_int


height = get_int("Height: ")
if height < 0 or height > 9:
    exit()

for i in range(height):
    print((height - i) * " ", end = "")
    print((i + 1) * "#")

