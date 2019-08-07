from cs50 import sys
from cs50 import cs50

def main():
    if(len(sys.argv) != 2):
        print("expected 1 commandline argument")
        sys.exit(1)
    word = cs50.get_string("plaintext: ")
    key = sys.argv[1]

    newWord = []

    i = 0
    while(i != len(word)):
        if(ord(word[i]) >= 97 and ord(word[i]) <= 122):
            newWord.append(chr(((int(ord(word[i])) - 97 + int(key)) % 26) + 97))
        elif(ord(word[i]) >= 65 and ord(word[i]) <= 90):
            newWord.append(chr(((int(ord(word[i])) - 65 + int(key)) % 26) + 65))
        else:
            newWord.append(word[i])
        i = i + 1

    i = 0

    print("ciphertext:", ''.join(newWord))

if __name__ == "__main__":
    main()