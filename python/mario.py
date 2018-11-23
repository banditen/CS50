from cs50 import get_int


def main():

    # Prompt user for the pyramid height
    height = get_int("Height: ")

    # Set height limit
    while not height in range(0, 24):
        height = get_int("Height: ")

    # For each row
    for row in range(height):

        # Print spaces
        for space in range(height - row - 1):

            print(" ", end="")

        # Print left half
        for lefthash in range(height - row, height + 1):

            print("#", end="")

        # Print gap
        print("  ", end="")

        # Print right half
        for righthash in range(height - row, height + 1):

            print("#", end="")

        # Print a new line
        print()


if __name__ == "__main__":
    main()
