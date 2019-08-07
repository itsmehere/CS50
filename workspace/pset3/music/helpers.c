// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>
#include <stdio.h>
#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int numerator = fraction[0] - '0';
    int denominator = fraction[2] - '0';

    return numerator * (8 / denominator);
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    int octave = note[strlen(note) - 1] - '0';
    float freq = 440.0;

    switch (note[0])
    {
        case 'A':
            break;
        case 'B':
            freq = freq * pow(2.0, 2.0 / 12.0);
            break;
        case 'C':
            freq = freq / pow(2.0, 9.0 / 12.0);
            break;
        case 'D':
            freq = freq / pow(2.0, 7.0 / 12.0);
            break;
        case 'E':
            freq = freq / pow(2.0, 5.0 / 12.0);
            break;
        case 'F':
            freq = freq / pow(2.0, 4.0 / 12.0);
            break;
        case 'G':
            freq = freq / pow(2.0, 2.0 / 12.0);
            break;
    }

    if (octave > 4)
    {
        for (int i = 0; i < octave - 4; i++)
        {
            freq = freq * 2.0;
        }
    }
    else if (octave < 4)
    {
        for (int i = 0; i < 4 - octave; i++)
        {
            freq = freq / 2.0;
        }
    }

    if (note[1] == 'b')
    {
        freq = freq / (pow(2.0, (1.0 / 12.0)));
    }
    else if (note[1] == '#')
    {
        freq = freq * (pow(2.0, (1.0 / 12.0)));
    }

    int frequencyToReturn = round(freq);
    return frequencyToReturn;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (strlen(s) == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}