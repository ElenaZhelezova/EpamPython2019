"""
Представьте, что вы пишите программу по формированию и выдачи комплексных обедов для сети столовых, которая стала
расширяться и теперь предлагает комплексные обеды для вегетарианцев, детей и любителей китайской кухни.

С помощью паттерна "Абстрактная фабрика" вам необходимо реализовать выдачу комплексного обеда, состоящего из трёх
позиций (первое, второе и напиток).
В файле menu.yml находится меню на каждый день, в котором указаны позиции и их принадлежность к
определенному типу блюд.

"""
import yaml

with open("menu.yml", 'r') as stream:
    menu = yaml.safe_load(stream)


class GetDinner:
    def get_first_course(self, day):
        return menu[day]['first_courses']

    def get_second_course(self, day):
        return menu[day]['second_courses']

    def get_drink(self, day):
        return menu[day]['drinks']


class VeganDinner(GetDinner):
    def get_first_course(self, day):
        return super().get_first_course(day)['vegan']

    def get_second_course(self, day):
        return super().get_second_course(day)['vegan']

    def get_drink(self, day):
        return super().get_drink(day)['vegan']


class KidDinner(GetDinner):
    def get_first_course(self, day):
        return super().get_first_course(day)['child']

    def get_second_course(self, day):
        return super().get_second_course(day)['child']

    def get_drink(self, day):
        return super().get_drink(day)['child']


class ChineseDinner(GetDinner):
    def get_first_course(self, day):
        return super().get_first_course(day)['china']

    def get_second_course(self, day):
        return super().get_second_course(day)['china']

    def get_drink(self, day):
        return super().get_drink(day)['china']


def client_code(factory, day):
    first_course = factory.get_first_course(day)
    second_course = factory.get_second_course(day)
    drink = factory.get_drink(day)
    dinner = {'first_course': first_course, 'second_course': second_course, 'drink': drink}
    print(f"Your dinner for {day} is {dinner}")


client_code(VeganDinner(), 'Monday')
client_code(KidDinner(), 'Wednesday')
client_code(ChineseDinner(), 'Saturday')