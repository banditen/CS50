#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main(void)
{
    // Prompt user's name
    string name = get_string();

    // Print the first char of that name as capitalized
    printf("%c", toupper(name[0]));

    // Create a loop for going through other names/words
    for (int i = 0, n = strlen(name); i < n; i++)
    {
        // If the string has a space or is not equal to \0
        if (name[i] == ' ' && name[i + 1] != '\0')
        {
            // Then print the first char of the second name as toupper
            printf("%c", toupper(name[i + 1]));
        }
    }
    printf("\n");
}