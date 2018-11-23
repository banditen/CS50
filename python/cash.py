from cs50 import get_float
from math import floor


def main():

    while True:
        change_owed = get_float("Change owed: ")
        coins = floor(change_owed * 100)

        if coins > 0:
            break

    quarter = coins // 25
    dime = (coins % 25) // 10
    nickel = ((coins % 25) % 10) // 5
    penny = (coins % 25) % 10 % 5

    print(f"{quarter + dime + nickel + penny}")


if __name__ == "__main__":
    main()




