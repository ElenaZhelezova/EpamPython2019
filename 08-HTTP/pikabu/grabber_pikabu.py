import json
import requests
from bs4 import BeautifulSoup
from collections import Counter


class Grabber:
    HOME = "https://pikabu.ru"                    # адрес страницы
    HEADERS = {                                    # заголовки которые браузер отдает
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Csrf-Token": input('XCSRF'),                                    # проверяет, что именно этот пользователь делает запрос
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Referer": "https://pikabu.ru/"
    }

    def __init__(self, username, password):
        self.session = requests.Session()         # создадим сессию
        self.session.headers = self.HEADERS      # пропишем заголовки, чтобы прикинуться браузером
        self.auth(username, password)            # авторизация

    def get_page(self, url):
        return self.session.get(url).text      # получим содержание страницы

    def auth(self, username, password):
        page = self.get_page(self.HOME)      # зайдем и пропишем куки

        cook_phpsess = {                     # некоторые куки допишем руками т к капча
            "name": "PHPSESS",
            "value": input("phpsess")
        }
        self.session.cookies.set(**cook_phpsess)

        cook_ulfs = {
            "name": "ulfs",
            "value": input("ulfs")
        }
        self.session.cookies.set(**cook_ulfs)

        data = {                                         # данные, отправляемые для авторизации
            "mode": "login",
            "username": username,
            "password": password,
            "g-recaptcha-response": input("g-rec")
            }
        self.session.post('https://pikabu.ru/ajax/auth.php', data=data)   # закидываем данные в скрипт авторизации


def parse_datafile(filename):

    with open(filename, 'rb') as fn:
        soup = BeautifulSoup(fn.read(), features='lxml')           # открываем\читаем файл

    tag_words = []

    articles = soup.find_all('article', limit=105)            # находим все статьи

    for article in articles:                         # рекламные статьи не смотрим
        if article.find('script'):
            continue

        story_tags = article.find('div', {'class': 'story__tags tags'})       # в каждой статье находим блок с тэгами
        tags = story_tags.find_all('a', {'class': 'tags__tag'})              # а потом и имена тэгов
        for tag in tags:
            word = tag.get('data-tag')
            if word is not None:
                tag_words.append(word)            # добавляем имя тэга в список

    return Counter(tag_words).most_common(10)         # возвращаем 10 самых частых


def get_datafile():
    grabber = Grabber('elena.zhelezova@gmail.com', 'cde3vfr4B')    # авторизация
    page_json = grabber.get_page("https://pikabu.ru")       # получаем первую страницу
    page_1 = json.loads(page_json)
    page_1 = page_1['html']

    page_file = 'page.html'                               # запись контента в файл
    with open(page_file, 'w') as p:
        p.write(page_1)

    for n in range(2, 6):                                 # дозапись еще 4 страниц
        next_page_json = grabber.get_page(f"https://pikabu.ru/?twitmode=1&of=v2&page={n}&_={input('_')}")
        next_page = json.loads(next_page_json)
        for i in next_page['data']['stories']:
            with open(page_file, 'a') as p:
                p.write(i['html'])

    return page_file


def main():
    page_file = get_datafile()   # получаем скачаные страницы с статьями

    parse_data = parse_datafile(page_file)  # парсинг статей

    with open('most_common_tags', 'w') as ct:    # запись топ-10 тэгов
        for i in parse_data:
            ct.write(str(i[0]))             # только имен тэгов
            ct.write('\n')


if __name__ == '__main__':
    main()
