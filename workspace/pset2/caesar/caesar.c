#include <stdio.h>
#include <cs50.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("expected 1 commandline argument\n");
        return 1;
    }

    string message = get_string("plaintext: ");
    int k = atoi(argv[1]);
    int i = 0;
    while (message[i] != '\0')
    {
        if (message[i] >= 'a' && message[i] <= 'z')
        {
            message[i] = (((message[i] - 97 + k) % 26) + 97);
        }
        else if (message[i] >= 'A' && message[i] <= 'Z')
        {
            message[i] = (((message[i]  - 65 + k) % 26) + 65);
        }
        i++;
    }
    i = 0;

    printf("ciphertext: ");
    while (message[i] != '\0')
    {
        printf("%c", message[i]);
        i++;
    }
    printf("\n");
    return 0;
}
