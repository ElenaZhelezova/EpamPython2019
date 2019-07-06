"""
Реализовать дескриптор, кодирующий слова с помощью шифра Цезаря

"""

import string


class ShiftDescriptor:
    def __init__(self, shift_value):
        self.shift_value = shift_value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value
        new_value = ""
        for v in value:
            v_index = string.ascii_lowercase.find(v)
            new_value += string.ascii_lowercase[(v_index + self.shift_value) % (len(string.ascii_lowercase))]
        self.value = new_value
        return self.value


class CeasarSipher:
    message = ShiftDescriptor(4)
    another_message = ShiftDescriptor(7)


if __name__ == '__main__':
    a = CeasarSipher()
    a.message = 'abc'
    a.another_message = 'hello'

    assert a.message == 'efg'
    assert a.another_message == 'olssv'

    a = CeasarSipher()
    a.message = 'abc'
    a.message = 'dsff'

    a.message = 'abcdf'
    a.message = 'dsffsaa'

    print(a.__dict__)
    print(a.abc)
