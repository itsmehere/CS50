#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 0 || height > 23);

    int leftBlanks = height - 1;
    int rightBlanks = (height * 2) - (height - 1);
    int j;

    for (int i = 0; i < height; i++)
    {
        for (j = 0; j < (height * 2) + 2; j++)
        {
            if (j < height)
            {
                if (j > leftBlanks - 1)
                {
                    printf("#");
                }
                else
                {
                    printf(" ");
                }
            }

            if (j == height)
            {
                printf("  ");
            }

            if (j > height)
            {
                if (j <= rightBlanks)
                {
                    printf("#");
                }
            }
        }
        leftBlanks--;
        if (j > height)
        {
            rightBlanks++;
        }
        printf("\n");
    }
}