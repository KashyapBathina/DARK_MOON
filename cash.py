# TODO
from cs50 import get_float

count = 0

while True:
    owed = get_float("How much change is owed: ")
    if owed > 0:
        break
    cents = round(owed * 100)

while owed >= 25:
    owed = owed - 25
    count += 1

while owed >= 10:
    owed = owed - 10
    count += 1

while owed >= 5:
    owed = owed - 5
    count += 1

while owed >= 1:
    owed = owed - 1
    count += 1

print(count)