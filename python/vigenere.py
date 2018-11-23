from cs50 import get_string
import sys
import string


def main():

    # Set command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python vigenere.py key")
        exit(1)
    elif not sys.argv[1].isalpha():
        print("Use only alphabetical characters!")
        exit(1)

    # Initialize 'key' as the command-line input
    key = sys.argv[1]

    # Prompt input from user
    plaintext = get_string("Plaintext: ")

    # Set encryption rules
    cipher = encrypt(plaintext, key)

    print(f"ciphertext: {cipher}")


def encrypt(message, key):

    # Initialize variables needed for encryption
    index = 0
    message = list(message)
    length = len(key)
    ascii_len = len(string.ascii_lowercase)
    key = [ord(name.upper()) - ord("A") for name in key]

    # Perform calculation based on capitalized or lowercase characters
    for i, name in enumerate(message):

        if name.isalpha():

            # 'Formula' from vigenere.c, based on ASCII table
            if name.isupper():
                message[i] = chr((ord(name) - ord("A") + key[index]) % ascii_len + ord("A"))
            else:
                message[i] = chr((ord(name) - ord("a") + key[index]) % ascii_len + ord("a"))

            index = (index + 1) % length

    # Store encryption in the list
    message = "".join(message)

    # Return encryption to output
    return message


if __name__ == "__main__":
    main()