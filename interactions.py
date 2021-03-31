from math import inf
import os

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def getInt(default=1, expected="choice", limit: int = inf):
    print(f"Enter {expected} ({default} by default):")

    while True:
        i = input("> ")

        if i == "":
            return default

        try:
            val = int(i)

            if val > 0 and val <= limit:
                return val

            print(f"Error: {i} is not a valid {expected}, leave blank or enter a valid {expected}:")

        except ValueError:
            print(f"'{i}' is not an integer, leave blank or enter a valid {expected}:")


def enumerateMenu(choices):

    for i, elt in enumerate(choices):
        print(f"\t({i+1}) - {elt}")

    print()