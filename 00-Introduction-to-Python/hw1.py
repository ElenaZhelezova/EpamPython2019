# -*- coding: utf-8 -*-

"""
Реализуйте метод, определяющий, является ли одна строка
перестановкой другой. Под перестановкой понимаем любое
изменение порядка символов. Регистр учитывается, пробелы
являются существенными.
"""

from collections import Counter


def is_permutation(a: str, b: str) -> bool:
    # Нужно проверить, являются ли строчки 'a' и 'b' перестановками
    return Counter(a) == Counter(b)


assert is_permutation('baba', 'abab')
assert is_permutation('abbba', 'abab')