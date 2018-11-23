#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

/**
 * Caesar.c
 * This program encrypts one's inputted plaintext into
 * ciphertext. The program accepts only single command-line
 * arguments, and returns false if the user inputs something
 * else. Try it out!
 * */

int main(int argc, char **argv)
{
    // Sets command-line arguments to 1

    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }

    // Converts a string to an actual integer

    int k = atoi(argv[1]);

    // Only positive values are accepted

    if (k < 0)

    {
        printf("Key must be positive \n");
    }

    // Prompt user for input

    string name = get_string("plaintext: ");
    printf("ciphertext: ");

    for (int i = 0, n = strlen(name); i < n; i++)
    {
        // If the input includes lowercase letters

        if (islower(name[i]))

            // Perform alphabet wrapping with lowercase letters

        {
            printf("%c", (name[i] - 'a' + k) % 26 + 'a');
        }

        // If the input includes lowercase letters

        else if (isupper(name[i]))

            // Perform alphabet wrapping with capitalized letters
        {
            printf("%c", (name[i] - 'A' + k) % 26 + 'A');
        }

        // If the input includes something else, print as it is

        else

        {
            printf("%c", name[i]);
        }
    }

    // Print new line and exit program

    printf("\n");
    return 0;
}