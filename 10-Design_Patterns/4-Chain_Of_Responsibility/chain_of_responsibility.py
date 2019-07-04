"""
С помощью паттерна "Цепочка обязанностей" составьте список покупок для выпечки блинов.
Необходимо осмотреть холодильник и поочередно проверить, есть ли у нас необходимые ингридиенты:
    2 яйца
    300 грамм муки
    0.5 л молока
    100 грамм сахара
    10 мл подсолнечного масла
    120 грамм сливочного масла

В итоге мы должны получить список недостающих ингридиентов.
"""


class Pancakes:
    def __init__(self, eggs, flour, milk, sugar, veg_oil, butter):
        self.eggs = eggs
        self.flour = flour
        self.milk = milk
        self.sugar = sugar
        self.veg_oil = veg_oil
        self.butter = butter


class BaseHandler:
    _next = None

    def set_next_handler(self, next_handler):
        self._next = next_handler
        return self._next

    def handler(self, request):
        if self._next:
            return self._next.handler(request)
        else:
            return


class CheckEggs(BaseHandler):
    def handler(self, pancakes):
        if pancakes.eggs < 3:
            print(f"You need {3 - pancakes.eggs} egg(s)")
        return super().handler(pancakes)


class CheckFlour(BaseHandler):
    def handler(self, pancakes):
        if pancakes.flour < 300:
            print(f"You need {300 - pancakes.flour} gramms of flour")
        return super().handler(pancakes)


class CheckMilk(BaseHandler):
    def handler(self, pancakes):
        if pancakes.milk < 500:
            print(f"You need {500 - pancakes.milk} ml of milk")
        return super().handler(pancakes)


class CheckSugar(BaseHandler):
    def handler(self, pancakes):
        if pancakes.sugar < 100:
            print(f"You need {100 - pancakes.sugar} gramms of sugar")
        return super().handler(pancakes)


class CheckVegOil(BaseHandler):
    def handler(self, pancakes):
        if pancakes.veg_oil < 10:
            print(f"You need {10 - pancakes.veg_oil} ml of vegetable oil")
        return super().handler(pancakes)


class CheckButter(BaseHandler):
    def handler(self, pancakes):
        if pancakes.butter < 120:
            print(f"You need {120 - pancakes.butter} gramms of butter")
        return super().handler(pancakes)


pancake_1 = Pancakes(3, 300, 500, 100, 10, 120)
pancake_2 = Pancakes(4, 400, 600, 200, 30, 300)
pancake_3 = Pancakes(2, 200, 400, 50, 0, 20)

check_products = CheckEggs()
check_products.set_next_handler(CheckFlour()).set_next_handler(CheckMilk()).set_next_handler(
    CheckSugar()).set_next_handler(CheckVegOil()).set_next_handler(CheckButter())
print("1st check")
check_products.handler(pancake_1)
print("2nd check")
check_products.handler(pancake_2)
print("3rd check")
check_products.handler(pancake_3)