#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/**
 * Vigenere.c
 * This program encrypts one's inputted plaintext into ciphertext,
 * but with an additional twist. The program accepts only single
 * command-line arguments and a string command, and returns false
 * if the user inputs something else. Try it out!
 * */

int main(int argc, char **argv)
{
    // Sets command-line arguments to 1

    if (argc != 2)
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }

    // If command-line argument is anything else than alphabetic

    else
    {
        for (int i = 0, length = strlen(argv[1]); i < length; i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("Invalid key\n");
                return 1;
            }
        }
    }

    // Store 'k' as string in array and declare 'length' as the length of 'k'

    string k = (argv[1]);
    int length = strlen(k);

    // Prompt user for input

    string name = get_string("plaintext: ");
    printf("ciphertext: ");

    // Loop through the input

    for (int i = 0, index = 0, n = strlen(name); i < n; i++)
    {

        // Checks if input is alphabetic

        if (isalpha(name[i]))
        {

            // If input includes lowercase letters

            if (islower(name[i]))

            {
                // Perform wrapping calculation with lowercase letters

                printf("%c", (name[i] - 'a' + toupper(k[index]) - 'A') % 26 + 'a');
            }

            // If the input includes capitalized letters

            else if (isupper(name[i]))

            {
                // Perform wrapping calculation with capitalized letters

                printf("%c", (name[i] - 'A' + toupper(k[index]) - 'A') % 26 + 'A');
            }
            index = (index + 1) % length;
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