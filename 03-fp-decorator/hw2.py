def is_armstrong(number):
    return number == sum([int(i)**len(str(number)) for i in str(number)])


assert is_armstrong(153) == True   # 'Число Армстронга'
assert is_armstrong(10) == False   # 'Не число Армстронга'