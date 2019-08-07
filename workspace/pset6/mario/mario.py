from cs50 import get_int

height = get_int("Height: ")

while(height < 0 or height >= 24):
    height = get_int("Height")

leftBlanks = height - 1
rightBlanks = (height * 2) - (height - 1)

i = 0
j = 0

for i in range(height):

    for j in range((height * 2) + 2):

        if(j < height):

            if(j > leftBlanks - 1):

                print("#", end="")

            else:

                print(" ", end="")

        if(j == height):

            print("  ", end="")

        if(j > height):

            if(j <= rightBlanks):

                print("#", end="")

    leftBlanks = leftBlanks - 1

    if(j > height):

        rightBlanks = rightBlanks + 1
    print("")