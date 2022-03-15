#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int main(void)
{
    // promt
    string text = get_string("Text: ");

    // letters
    int Letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];
        if (isalpha(c) != 0)
        {
            Letters++;
        }
    }


    // words
    int Words = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            Words++;
        }
    }



    // sentences
    int Sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            Sentences ++;
        }
    }


    // calculations
    float L = ((float)Letters / (float)Words) * 100;
    float S = ((float)Sentences / (float)Words) * 100;
    float subindex = 0.0588 * L - 0.296 * S - 15.8;
    int index = round(subindex);
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

}