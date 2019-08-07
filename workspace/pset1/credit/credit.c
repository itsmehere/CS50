#include <stdio.h>
#include <cs50.h>

bool isValidChecksum(int cardNumber[], int cardNumLength);

int main(void)
{
    long long cardNum = get_long_long("Number : ");
    long long remainingCardNum = cardNum;

    int cardReversedDigits[20] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    int i = 0;

    while (remainingCardNum > 9)
    {
        cardReversedDigits[i] = remainingCardNum % 10;
        remainingCardNum = remainingCardNum / 10;
        i++;
    }
    cardReversedDigits[i] = remainingCardNum;
    int cardDigits[i + 1];
    int cardNumLen = i + 1;

    int k = 0;
    for (int j = i; j >= 0; j--)
    {
        cardDigits[k] = cardReversedDigits[j];
        k++;
    }

    if (cardNumLen != 13 && cardNumLen != 15 && cardNumLen != 16)
    {
        printf("INVALID\n");
        return 0;
    }

    if (!isValidChecksum(cardDigits, cardNumLen))
    {
        printf("INVALID\n");
        return 0;
    }

    if (cardNumLen == 15 && cardDigits[0] == 3 && (cardDigits[1] == 4 || cardDigits[1] == 7))
    {
        printf("AMEX\n");
        return 0;
    }

    if (cardNumLen == 13 && cardDigits[0] == 4)
    {
        printf("VISA\n");
        return 0;
    }

    if (cardNumLen == 16)
    {
        if (cardDigits[0] == 4)
        {
            printf("VISA\n");
            return 0;
        }
        if (cardDigits[0] == 5 &&
            (cardDigits[1] == 1 || cardDigits[1] == 2 || cardDigits[1] == 3 || cardDigits[1] == 4 || cardDigits[1] == 5))
        {
            printf("MASTERCARD\n");
            return 0;
        }
    }
    printf("INVALID\n");
    return 0;
}


bool isValidChecksum(int cardNumber[], int cardNumLength)
{
    int sum = 0;
    int product = 0;

    for (int i = cardNumLength - 2; i >= 0; i = i - 2)
    {
        product = cardNumber[i] * 2;
        if (product > 9)
        {
            sum = sum + (product % 10);
            sum = sum + (product / 10);
        }
        else
        {
            sum = sum + product;
        }
    }

    for (int i = cardNumLength - 1; i >= 0; i = i - 2)
    {
        sum = sum + cardNumber[i];
    }

    if (sum % 10 == 0)
    {
        return true;
    }
    return false;
}