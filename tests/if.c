#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main (void)
{
    string s = {'g', 'u', 's', 'd', 'i', 'm'};
    s[5] = 's';

    for (int i = 1; i < 2; i = i + 2)
    {
        s[i] = s[i - 2];
        printf("%i", s);

    }
}