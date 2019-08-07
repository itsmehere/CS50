#include <stdio.h>
#include <cs50.h>
#include <string.h>

bool isLower(char c);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("expected 1 commandline argument\n");
        return 1;
    }
    string keyword = argv[1];
    int i = 0;
    while (keyword[i] != '\0')
    {
        if ((keyword[i] >= 'A' && keyword[i] <= 'Z') || (keyword[i] >= 'a' && keyword[i] <= 'z'))
        {
            i++;
        }
        else
        {
            printf("Only letters can be part of the keyword.\n");
            return 1;
        }
    }
    string message = get_string("plaintext: ");

    i = 0;
    int j = 0;
    while (message[i] != '\0')
    {
        if ((message[i] >= 'A' && message[i] <= 'Z') || (message[i] >= 'a' && message[i] <= 'z'))
        {
            int k = 0;
            if (isLower(keyword[j]))
            {
                k = keyword[j] - 'a';
            }
            else
            {
                k = keyword[j] - 'A';
            }
            if (isLower(message[i]))
            {
                message[i] = (message[i] - 'a' + k) % 26 + 'a';
            }
            else
            {
                message[i] = (message[i] - 'A' + k) % 26 + 'A';
            }
            j++;
        }
        i++;
        if (j == strlen(keyword))
        {
            j = 0;
        }
    }
    printf("ciphertext: %s\n", message);
}

bool isLower(char c)
{
    if (c >= 'a' && c <= 'z')
    {
        return true;
    }
    return false;
}