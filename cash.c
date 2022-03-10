#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int cents;
    do
    {
        cents = get_int("Enter your change: ");
    }
    while (cents <= 0);

    int coins = 0;

    while(cents >= 25)
        {
            cents = cents - 25;
            coins ++;
        }
    while(cents >= 10)
        {
            cents = cents - 10;
            coins++;
        }
    while(cents >= 5)
        {
            cents = cents - 5;
            coins++;
        }
    while(cents >= 1)
        {
            cents = cents - 1;
            coins++;
        }

        printf("You will need at least %i", coins);
}