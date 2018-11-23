#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Determine variables
    int height, line, space, hash;

    // Set height limit to 23
    do {
        printf("Height: ");
        height = get_int();
    }
    while (height < 0 || height > 23);

    // Print lines based on height
    for (line = 1; line <= height; line++)
    {
        // Print spaces
        for (space = 0; space < (height - line); space++)
        {
            printf(" ");
        }

        // Print hashes on left
        for (hash = 0; hash < line; hash++)
        {
            printf("#");
        }

        // Print gap
        printf("  ");

        // Print hashes on right
        for (hash = 0; hash < line; hash++)
        {
            printf("#");
        }

        printf("\n");
    }
}