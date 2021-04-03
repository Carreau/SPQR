"""
S.P.Q.R

Senātus Populusque Rōmānus
^       ^      ^   ^

The Senate and People of Rome

Just a Library to allow you be backward compatible with old numeral systems.
"""


__version__ = "0.0.6"

import copy


class RomanNumeral:
    def __init__(self, val):
        if type(val) is list:
            self.stack = val
        elif type(val) is str and len(val) > 1:
            self.stack = val.split()
        else:
            self.stack = [val]

    def _comb(self, other):
        t_stack = copy.copy(other.stack)
        t_stack.extend(self.stack)
        self.stack = t_stack
        return self

    def __getattr__(self, val):
        R = RomanNumeral(val)
        return R._comb(self)

    def __repr__(self):
        return int_to_roman(self._intval())

    def _intval(self):
        return roman_to_int("".join(self.stack))

    def __mul__(self, other):
        return RomanNumeral(int_to_roman(self._intval() * other._intval()).split())

    def __add__(self, other):
        return RomanNumeral(int_to_roman(self._intval() + other._intval()).split())

    def __sub__(self, other):
        return RomanNumeral(int_to_roman(self._intval() - other._intval()).split())


def int_to_roman(input):
    """
    Convert an integer to Roman numerals.

    Examples:
    >>> int_to_roman(0)
    Traceback (most recent call last):
    ValueError: Argument must be between 1 and 3999

    >>> int_to_roman(-1)
    Traceback (most recent call last):
    ValueError: Argument must be between 1 and 3999

    >>> int_to_roman(1.5)
    Traceback (most recent call last):
    TypeError: expected integer, got <type 'float'>

    >>> for i in range(1, 21): print int_to_roman(i)
    ...
    I
    II
    III
    IV
    V
    VI
    VII
    VIII
    IX
    X
    XI
    XII
    XIII
    XIV
    XV
    XVI
    XVII
    XVIII
    XIX
    XX
    >>> print int_to_roman(2000)
    MM
    >>> print int_to_roman(1999)
    MCMXCIX
    """
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
    result = ""
    for i in range(len(ints)):
        count = int(input / ints[i])
        result += nums[i] * count
        input -= ints[i] * count
    return result


def roman_to_int(input):
    """
    Convert a roman numeral to an integer.

    >>> r = range(1, 4000)
    >>> nums = [int_to_roman(i) for i in r]
    >>> ints = [roman_to_int(n) for n in nums]
    >>> print r == ints
    1

    >>> roman_to_int('VVVIV')
    Traceback (most recent call last):
     ...
    ValueError: input is not a valid roman numeral: VVVIV
    >>> roman_to_int(1)
    Traceback (most recent call last):
     ...
    TypeError: expected string, got <type 'int'>
    >>> roman_to_int('a')
    Traceback (most recent call last):
     ...
    ValueError: input is not a valid roman numeral: A
    >>> roman_to_int('IL')
    Traceback (most recent call last):
     ...
    ValueError: input is not a valid roman numeral: IL
    """

    input = input.upper()
    nums = ["M", "D", "C", "L", "X", "V", "I"]
    ints = [1000, 500, 100, 50, 10, 5, 1]
    places = []
    for c in input:
        if not c in nums:
            raise ValueError("input is not a valid roman numeral: %s" % input)
    for i in range(len(input)):
        c = input[i]
        value = ints[nums.index(c)]
        # If the next place holds a larger number, this value is negative.
        try:
            nextvalue = ints[nums.index(input[i + 1])]
            if nextvalue > value:
                value *= -1
        except IndexError:
            # there is no next place.
            pass
        places.append(value)
    sum = 0
    for n in places:
        sum += n
    # Easiest test for validity...
    if int_to_roman(sum) == input:
        return sum
    else:
        raise ValueError("input is not a valid roman numeral: %s" % input)


V = RomanNumeral("V")
I = RomanNumeral("I")
X = RomanNumeral("X")
C = RomanNumeral("C")
M = RomanNumeral("M")
