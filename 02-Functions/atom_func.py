"""
Напишите реализацию функции atom, которая инкапсулирует некую переменную,
предоставляя интерфейс для получения и изменения ее значения,
таким образом, что это значение нельзя было бы получить или изменить
иными способами.get_value - позволяет получить значение хранимой переменной;

Пусть функция atom принимает один аргумент, инициализирующий хранимое значение
(значение по умолчанию, в случае вызова atom без аргумента - None),
а возвращает 3 функции - get_value, set_value, process_value, delete_value,такие, что:

set_value - позволяет установить новое значение хранимой переменной, возвращает его;
process_value - принимает в качестве аргументов сколько угодно функций и последовательно
    (в порядке перечисления аргументов) применяет эти функции
    к хранимой переменной, обновляя ее значение (перезаписывая получившийся
    результат) и возвращая получишееся итоговое значение.
delete_value - удаляет переменную, значение храние в ней и функции get_value,
    set_value, process_value. Если получится, то и delete_value
"""


def atom(value=None):

    def get_value():
        return value

    def set_value(update_value):
        nonlocal value
        value = update_value

    def process_value(*funcs):
        nonlocal value
        for func in funcs:
            value = func(value)

    def delete_value():
        nonlocal value, get_value, set_value, process_value
        del value
        del get_value
        del set_value
        del process_value

        del globals()['atom']

    return get_value, set_value, process_value, delete_value
