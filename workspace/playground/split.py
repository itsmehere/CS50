from cs50 import sys

def compareLines(lines1, lines2):
    i = 0
    identicalLines = []
    for line1 in lines1:
        for line2 in lines2:
            if(line1 == line2):
                if (len(line1) > 0):
                    identicalLines.append(line1)
                else:
                    identicalLines.append("")
    return identicalLines

def main():
    a = "hello World\nhow are you?\I am ok"
    b = "hello world\nblahblah\nI am ok"
    alines = a.split("\n")
    blines = b.split("\n")

    if len(alines) < len(blines):
        output = compareLines(alines, blines)
    else:
        output = compareLines(blines, alines)

    print(''.join(output))

if __name__ == "__main__":
    main()