from cs50 import sys

word = sys.argv[1]
key = sys.argv[2]

newWord = []
newWord.append(chr(ord(word[0]) + int(key)))

