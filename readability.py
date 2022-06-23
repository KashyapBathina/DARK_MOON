# TODO
from cs50 import get_string

letters = 0
words = 1
sentences = 0

text = get_string("Text: ")

for i in range(len(text)):
    if(text[i].isalpha()):
        letters += 1

    if (text[i].isspace()):
        words += 1

    if (text[i] == "." or text[i] == "!" or text[i] == "?"):
        sentences += 1

calculation = 0.0588 * (letters / words * 100) - 0.296 * (sentences / words * 100) - 15.8
level = round(calculation)

if level < 1:
    print("Before Grade 1")
elif level > 16:
    print("Grade 16+")
else:
    print(f"Grade {level}")
