#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Prompt user for minutes in the shower
    int x = get_int("Minutes: ");

    // Set the multiplier to 12
    int y = 12;

    // Perform calculation
    printf("Bottles: %i\n", x * y);
}