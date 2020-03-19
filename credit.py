from cs50 import get_int


def main():
    while True:
        cc = get_int("Number: ")
        if (cc > 0 and cc <= 9999999999999999):
            break
    # getting digits for final card check, starting at 1 instead of 0, like problem text
    d16 = getDigit(cc, 15)
    d15 = getDigit(cc, 14)
    d14 = getDigit(cc, 13)
    d13 = getDigit(cc, 12)

    # luhn valid cc numbers are filtered by brand
    if (luhn(cc) != 1):
        print("INVALID")
    elif (d16 == 0 and (d15 == 3) and ((d14 == 4) or (d14 == 7))):
        print("AMEX")
    elif ((d16 == 5) and ((d15 == 1) or (d15 == 2) or (d15 == 3) or (d15 == 4) or (d15 == 5))):
        print("MASTERCARD")
    elif (d16 == 4):
        print("VISA")
    elif ((d16 == 0) and (d15 == 0) and (d14 == 0) and (d13 == 4)):
        print("VISA")
    else:
        print("INVALID")

# gets digit from cc number, must be a more pythonic way of doing this


def getDigit(number, place):
    tensPlaceHigher = pow(10, (place + 1))
    tensPlace = pow(10, place)
    digit = int(((number % tensPlaceHigher) - (number % (tensPlace))) / tensPlace)
    return(digit)


# luhn's algorithm

def luhn(la):
    leftSum = 0
    rightSum = 0
    isLeft = 0
    for i in range(16):
        digit = getDigit(la, i)
        if (isLeft == 0):
            if (digit > 9):
                # add digits if there are two
                digit = ((digit - (digit % 10)) * .1) + (digit % 10)
            rightSum = int(rightSum + digit)
        else:
            digit = digit * 2
            if (digit > 9):
                # add digits if there are two
                digit = ((digit - (digit % 10)) * .1) + (digit % 10)
            leftSum = int(leftSum + digit)
        isLeft = not isLeft
    if (((leftSum + rightSum) % 10) == 0):
        valid = 1
    else:
        valid = 0
    return (valid)


main()