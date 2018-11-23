// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    // Converting string "X/Y" to integer

    int X = fraction[0] - '0';
    int Y = fraction[2] - '0';

    // Converting "X" to number of eights

    return (8 / Y) * X;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    int octave = note[strlen(note) - 1] - '0';

    // Determine f as frequency and eliminate ghost numbers

    double freq = 440.0;
    double fullnote = 2.0;
    double octavelength = 12.0;

    // Determine note based on letter

    if (note[0] == 'B')
    {
        freq *= (pow(fullnote, (2.0 / octavelength)));
    }
    else if (note[0] == 'C')
    {
        freq /= (pow(fullnote, (9.0 / octavelength)));
    }
    else if (note[0] == 'D')
    {
        freq /= (pow(fullnote, (7.0 / octavelength)));
    }
    else if (note[0] == 'E')
    {
        freq /= (pow(fullnote, (5.0 / octavelength)));
    }
    else if (note[0] == 'F')
    {
        freq /= (pow(fullnote, (4.0 / octavelength)));
    }
    else if (note[0] == 'G')
    {
        freq /= (pow(fullnote, (2.0 / octavelength)));
    }

    // Loop string octave to shift octave

    if (octave > 4)
    {
        for (int i = 0; i < octave - 4; i++)
        {
            freq *= fullnote;
        }
    }
    else if (octave < 4)
    {
        for (int i = 0; i < 4 - octave; i++)
        {
            freq /= fullnote;
        }
    }

    // Adjust note for sharp or flat

    if (note[1] == '#')
    {
        freq *= (pow(fullnote, (1.0 / octavelength)));
    }
    else if (note[1] == 'b')
    {
        freq /= (pow(fullnote, (1.0 / octavelength)));
    }

    // Return frequency as int

    return round(freq);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    // If string s represents blank; return true, otherwise return false

    if (s[0] == '\0')
    {
        return true;
    }
    else
    {
        return false;
    }

}
