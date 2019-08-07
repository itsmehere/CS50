from cs50 import sys
from cs50 import get_string
from cs50 import cs50

def main():
    if(len(sys.argv) != 2):
        print("expected 1 commandline argument")
        sys.exit(1)
    keyword = sys.argv[1]
    if(keyword.isalpha() == False):
        print("expected only letters")
        sys.exit(1)
    word = cs50.get_string("plaintext: ")


    i = 0
    j = 0
    key = 0
    val = 0
    newWord = []
    while(i < len(word)):
        if((word[i] >= 'A' and word[i] <= 'Z') or (word[i] >= 'a' and word[i] <= 'z')):
            if (isLower(keyword[j])):
                key = ord(keyword[j]) - 97
            else:
                key = ord(keyword[j]) - 65

            if (isLower(word[i])):
                val = 97
            else:
                val = 65

            char = chr((ord(word[i]) - val + key) % 26 + val)
            newWord.append(char)

            j = j + 1
            if(j > len(keyword) - 1):
                j = 0
        else:
            newWord.append(word[i])
        i = i + 1

    print("ciphertext: ", end = "")
    print(''.join(newWord))


def isLower(c):
    if(ord(c) >= ord('a') and ord(c) <= ord('z')):
        return True
    return False

if __name__ == "__main__":
    main()
