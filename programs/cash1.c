#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // Determine variables
    float change;
    int cash;
    int calc = 0;

    // Prompt change owed
    do
    {
        change = get_float("Change owed: ");
    }
    while (change <= 0);

    // Convert change to int and round float to closest int
    cash = roundf(change * 100);

    // Perform calculation

    // No. quarters
    while (cash >= 25 || cash >=10 || cash >=5 || cash >=1 )
    {
        cash = cash - 25;
        calc++;
        cash = cash - 10;
        calc++;
        cash = cash - 5;
        calc++;
        cash = cash - 1;
        calc++;
    }

    printf("%i\n", calc);
}