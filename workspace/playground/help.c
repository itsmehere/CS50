// Helper functions for music

#include <cs50.h>

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
    int octave = note[strlen(note) - 1] - '0'
    float frequency = 440.0;

    switch(note[0]) {
        case 'A':
            break;
        case 'B':
            frequency = frequency *
        case 'C':

        case 'D':

        case 'E':

        case 'F':

        case 'G':
    }
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if(strlen(s) == 0){
        return true;
    } else {
        return false;
    }
}

/*
D4@1/8
D4@1/8
E4@1/4
D4@1/4
G4@1/4
F#4@1/2
D4@1/8
D4@1/8
E4@1/4
D4@1/4
A4@1/4
G4@1/2
D4@1/8
D4@1/8
D5@1/4
B5@1/4
G4@1/4
F#4@1/4
E4@1/4
C5@1/8
C5@1/8
B5@1/4
G4@1/4
A4@1/4
G4@1/2
*/