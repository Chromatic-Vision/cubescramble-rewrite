import random

def get_scramble():

    scramble = ""

    scramble += "UR" + random_rotation() + " "
    scramble += "DR" + random_rotation() + " "
    scramble += "DL" + random_rotation() + " "
    scramble += "UL" + random_rotation() + " "
    scramble += "U" + random_rotation() + " "
    scramble += "R" + random_rotation() + " "
    scramble += "D" + random_rotation() + " "
    scramble += "L" + random_rotation() + " "
    scramble += "ALL" + random_rotation() + " "
    scramble += "y2"
    scramble += " "
    scramble += "U" + random_rotation() + " "
    scramble += "R" + random_rotation() + " "
    scramble += "D" + random_rotation() + " "
    scramble += "L" + random_rotation()
    scramble += random_pins()

    return scramble

def random_rotation():

    res = ""
    number = random.randint(0, 6)

    res += str(number)

    if 0 < number < 6:
        if bool(random.getrandbits(1)):
            res += "+"
        else:
            res += "-"
    else:
        res += "+"

    return res

def random_pins():

    res = ""

    for i in range(4):
        if bool(random.getrandbits(1)):
            if i == 0:
                res += " UR"
            if i == 1:
                res += " DR"
            if i == 2:
                res += " DL"
            if i == 3:
                res += " UL"

    return res