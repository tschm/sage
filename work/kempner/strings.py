import pandas as pd
assert 0 ** 0 == 1


def T_matrix(strings, base=10):
    # the list of feasible ends
    feasible, infeasible  = __split_strings(strings)

    A = pd.DataFrame(index=feasible, columns=list(range(base)), data=0)

    ending = lambda digit, string : "{string}{digit}".format(digit=digit, string=string)

    for n, f in enumerate(feasible):
        for string in A.index:
            for digit in A.columns:
                if ending(digit, string).endswith(f):
                    A[digit][string] = n + 1 #if ending(digit, string).endswith(f)

    for excluded in infeasible:
        for string in A.index:
            for digit in A.columns:
                if ending(digit, string).endswith(excluded):
                    A[digit][string] = 0

    return A


def __split_strings(strings):
    # split a string, like "123" into ["","1","12"], note that the original string is missing
    def split_string(string):
        return [string[:w] for w in range(len(string))]

    if isinstance(strings, str):
        strings = [strings]

    # define an empty set
    endings = set([""])

    for string in sorted(strings, key=len):
        for word in split_string(string):
            if word in strings:
                # jumps out of the inner-most loop, needed in case such as "3", "335", etc.
                break
            else:
                endings.add(word)

    return sorted(list(endings), key=len), set(strings)