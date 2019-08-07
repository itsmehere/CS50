from cs50 import get_float
import math

numQuarters = 0
numDimes = 0
numNickels = 0
numPennies = 0

num = get_float("Change: ")

while(num < 0):
    num = get_float("Change: ")

change = round(num * 100)

if(change >= 25):
    numQuarters = math.floor(change / 25)
    change = change % 25
if(change >= 10):
    numDimes = math.floor(change / 10)
    change = change % 10
if(change >= 5):
    numNickels = math.floor(change / 5)
    change = change % 5

numPennies = change
print(f"{numQuarters + numDimes + numNickels + numPennies}")
