"""
Напишите функцию letters_range, которая ведет себя похожим на range образом,
однако в качестве start и stop принимает не числа, а буквы латинского алфавита
(в качестве step принимает целое число) и возвращает не перечисление чисел, а
список букв, начиная с указанной в качестве start (либо начиная с 'a',
если start не указан), до указанной в качестве stop с шагом step (по умолчанию
равным 1). Добавить возможность принимать словарь с заменами букв для подобия траслитерации.
Т.е. замена символов из оригинального алфавита другими, возможно несколькими символами.


Пример:
    >>> letters_range('b', 'w', 2)
    ['b', 'd', 'f', 'h', 'j', 'l', 'n', 'p', 'r', 't', 'v']

    >>> letters_range('g')
    ['a', 'b', 'c', 'd', 'e', 'f']

    >>> letters_range('g', 'p')
    ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']

    >>> letters_range('g', 'p', **{'l': 7, 'o': 0})
    ['g', 'h', 'i', 'j', 'k', 7, 'm', 'n', 0]

    >>> letters_range('p', 'g', -2)
    ['p', 'n', 'l', 'j', 'h']

    >>> letters_range('a')
    []
"""

import string
import doctest


def get_answer(start_val, stop_val, step_val=1, **kwargs):

    iter_string = string.ascii_lowercase
    index_start = iter_string.find(start_val)
    index_stop = iter_string.find(stop_val)

    if index_start == -1 or index_stop == -1:
        return

    answer_string = iter_string[index_start:index_stop:step_val]
    answer = list(answer_string)

    if not kwargs:
        return answer

    for key in kwargs:
        if key in answer:
            answer[answer.index(key)] = kwargs[key]

    return answer


def letters_range(*args, **kwargs):
    if len(args) == 1:
        return get_answer('a', args[0], **kwargs)

    return get_answer(*args, **kwargs)


if __name__ == "__main__":
    doctest.testmod()
