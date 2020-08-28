import re
def lines(a, b):
    """Return lines in both a and b"""
    same = set()
    for line1 in a.split('\n'):
        if (line1 in b.split('\n')):
            same.add(line1)
    # TODO
    return list(same)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    same = set()
    # Remove empty spaces and newlines from our string
    #a = re.sub(r"[\t\s]*", "", a)
    #b = re.sub(r"[\t\s]*", "", b)

    # Get longest and shortest string based on their lengths
    longest_str = a if (len(a) >= len(b)) else b 
    shortest_str = a if (len(a) <= len(b)) else b

    print('Shortest str')
    print(shortest_str)

    # Get all substrings removing the dublicates from a
    a_new = set()
    for i in range(0, (len(shortest_str)-(n-1))):
        a_new.add(shortest_str[i:(i+n)])

    # Make a_new a list
    a_new = list(a_new)

    # Check if substrings between in a and b match
    for i in a_new:
        if i in longest_str:
            same.add(i)
    # TODO
    return list(same)