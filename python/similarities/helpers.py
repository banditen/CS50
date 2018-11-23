from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    a_list = str.splitlines(a, keepends=False)
    b_list = str.splitlines(b, keepends=False)

    return compare(a_list, b_list)


def sentences(a, b):
    """Return sentences in both a and b"""

    a_list = sent_tokenize(a)
    b_list = sent_tokenize(b)

    return compare(a_list, b_list)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    a_list = substring(a, n)
    b_list = substring(b, n)

    return compare(a_list, b_list)


def substring(a, n):
    """Helper function for substring"""

    data = []

    length = len(a) - n + 1

    for i in range(length):
        data.append(a[i:n + i])

    return data


def compare(a, b):
    """Compares two lists for dulicates and returns commons)"""

    data = []

    # Iterate through lines
    for j in a:
        for k in b:
            if j == k and k not in data:
                data.append(k)

    return data

