#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    int numQuarters = 0;
    int numDimes = 0;
    int numNickels = 0;
    int numPennies = 0;
    float x = 0.0;
    do
    {
        x = get_float("Change owed: ");
    }
    while (x < 0);


    int change = round(x * 100);

    if (change >= 25)
    {
        numQuarters = change / 25;
        change = change % 25;
    }
    if (change >= 10)
    {
        numDimes = change / 10;
        change = change % 10;
    }
    if (change >= 5)
    {
        numNickels = change / 5;
        change = change % 5;
    }
    numPennies = change;
    printf("%d\n", numQuarters + numDimes + numNickels + numPennies);
}