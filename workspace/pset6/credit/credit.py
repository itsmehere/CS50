from cs50 import get_int
import math

def main():
    cardNum = get_int("Number : ");
    remainingCardNum = cardNum

    cardReversedDigits = []
    while(remainingCardNum > 9):
        cardReversedDigits.append(math.floor(remainingCardNum % 10));
        remainingCardNum = math.floor(remainingCardNum / 10);

    cardReversedDigits.append(remainingCardNum)
    cardNumLen = len(cardReversedDigits)

    if(cardNumLen != 13 and cardNumLen != 15 and cardNumLen != 16):
        print("INVALID")
        return 0

    cardDigits = []
    for j in range(cardNumLen - 1, -1, -1) :
        cardDigits.append(cardReversedDigits[j])

    if(cardNumLen == 15 and cardDigits[0] == 3 and (cardDigits[1] == 4 or cardDigits[1] == 7)):
        print("AMEX")
        return 0

    if(cardNumLen == 13 and cardDigits[0] == 4):
        print("VISA")
        return 0

    if(cardNumLen == 16):
        if (cardDigits[0] == 4):
            print("VISA\n");
            return 0;
        if (cardDigits[0] == 5 and (cardDigits[1] == 1 or cardDigits[1] == 2 or cardDigits[1] == 3 or cardDigits[1] == 4 or cardDigits[1] == 5)):
            print("MASTERCARD")
            return 0;

    print("INVALID")
    return 0;


def validCheck(card, cardLen):
    totalSum = 0
    product = 0;
    valid = None

    for i in range(cardLen - 2, -1, -2):
        product = card[i] * 2
        if(product > 9):
            totalSum = totalSum + (product % 10)
            totalSum = totalSum + math.floor(product / 10)
        else:
            totalSum = totalSum + product

    for j in range(cardLen - 1, -1, -2):
        totalSum = totalSum + card[j]

    if(totalSum % 10 == 0):
        valid = True
    else:
        valid = False

    return valid

if __name__ == "__main__":
    main()