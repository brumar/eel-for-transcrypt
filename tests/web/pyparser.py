import re

regex = r"backend\.([^(]+)\("

def notcommented(line):
    for car in line:
        if car == "#":
            return False
        if not car.isspace():
            return True

with open("frontendscrypt.py", "r") as f:
    
    vlist = [line.strip() for line in f if notcommented(line)]
    for match in re.finditer(regex, "".join(vlist), re.MULTILINE):
        print(match.group(1))
