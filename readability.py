# TODO
from cs50 import get_string

letters = 0
words = 0
sentences = 0

text = get_string("Text: ")

for i in range(len(text)):
    if(text[i].isalpha()):
        letters += 1

    if (text[i].isspace()):
        words +=1

    if (text[i] == "." or text[i] == "!" or text[i] == "?"):
        sentences += 1

level = 0.0588 * (letters / words * 100) - 0.296 * (sentences / words * 100) - 15.8

print(f"Grade {round(level)}")
