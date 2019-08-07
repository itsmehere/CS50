from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    similarLines = set()
    newA = a.split('\n')
    newB = b.split('\n')

    for aLine in newA:
        for bLine in newB:
            if(aLine == bLine):
                similarLines.add(aLine)
                break

    returnList = list(similarLines)
    return returnList

def sentences(a, b):
    """Return sentences in both a and b"""

    similarSent = set()
    newA = sent_tokenize(a)
    newB = sent_tokenize(b)

    for aSent in newA:
        for bSent in newB:
            if (aSent == bSent):
                similarSent.add(aSent)
                break

    returnList = list(similarSent)
    return returnList

def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    similarSubs = set()
    aSet = set()
    bSet = set()

    i = 0
    while i < len(a):
        if(len(a[i:i+n]) == n):
            aSet.add(a[i:i+n])
        i = i + 1

    i = 0
    while i < len(b):
        if(len(b[i:i+n]) == n):
            bSet.add(b[i:i+n])
        i = i + 1

    for aNum in aSet:
        for bNum in bSet:
            if(aNum == bNum):
                similarSubs.add(aNum)
                break

    return list(similarSubs)
