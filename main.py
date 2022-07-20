import os
import time
import datetime
import requests
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import re
from operator import itemgetter


def find_news():
    list_key = ['контрабанда рогов сайгака', 'контрабанда сайгачьих рогов', 'незаконный вывоз рогов сайгака',
                'контрабандный вывоз степных черепах', 'незаконный вывоз балобанов']

    list_news = {}
    k = 9
    for i in list_key:
        url = f'https://www.google.com/search?q={i}'
        page = requests.get(url)  # извлекаем данные в переменную
        soup = BeautifulSoup(page.text, 'html.parser')  # сохраняем html страницы, откуда будем извлекать данные
        search = soup.find_all('h3')
        search_data = soup.find_all('span')

        for j in range(len(search)):
            k += 1
            print(f'{search[j].get_text()}\n'
                  f'{search_data[k].get_text()}')

            soup.findAll('span', {"class": "item"})

    return


def open_href(href, request):
    url = f'{href}'
    page = requests.get(url)  # извлекаем данные в переменную
    soup = BeautifulSoup(page.text, 'html.parser')  # сохраняем html страницы, откуда будем извлекать данные
    description = soup.find('div', {'class': 'css-g5mtbi-Text'}).get_text()
    date_public = soup.find('span', {'class': 'css-19yf5ek'}).get_text()

    #Если объявление было выложено в этот день с надписью "Сегодня" ты форматируем в привычный формат
    if re.search(r'Сегодня', f"{date_public}"):
        date_public = datetime.datetime.today().strftime('%d %B %Y г.')
    return [request, date_public, href, description]


def main_foo():
    #list of requests
    list_of_requests = ['рога сайгака', 'степная черепаха',
                        'среднеазиатская черепаха', 'живая черепаха', 'продам черепаху']

    #list of result data
    list_result = []

    # ПЕРЕБОР ЗАПРОСОВ ИЗ list_of_requests
    for i in list_of_requests:
        j = 0
        url_olx = f'https://www.olx.kz/list/q-{i}/'
        page = requests.get(url_olx) #извлекаем данные в переменную
        soup = BeautifulSoup(page.text, 'html.parser') #сохраняем html страницы, откуда будем извлекать данные
        pages = len(soup.findAll('span', {"class": "item"})) #кол-во страниц, доступных для перелистывания

        if re.search(r'Не найдено', f"{soup.find_all('p')[3].get_text()}"):
            print('Не найдено объявлений')
            continue
        if re.search(r'Топ', f"{soup.find_all('h2')[0].get_text()}"):
            print(f"По запросу '{i}' {soup.find_all('p')[7].get_text()}")
        else:
            print(f"По запросу '{i}' {soup.find_all('h2')[1].get_text()}")


        #Если всего одна страница, то присвоем ей номер 1, чтобы цикл for начался
        if pages == 0:
            pages = 1

        for p in range(1, pages+1): #перебор всех страниц по запросу
            url_olx = f'https://www.olx.kz/list/q-{i}/?page={p}'
            page = requests.get(url_olx)
            soup = BeautifulSoup(page.text, 'html.parser')
            list_of_ads = soup.findAll('a', {"class": "thumb"}) # Кол-во объявлений на каждой странице
            for ad in list_of_ads: #Перебор всех объявлений со страницы и достаем от туда href
                if ad.__getattribute__('attrs')['href'] not in list_result: #Если ссылки еще нет в list_href, то добавляем
                    href = ad.__getattribute__('attrs')['href']
                    list_result.append(open_href(href, i))
            list_result = sorted(list_result, key=itemgetter(0, 1))
            print(f'Кол-во ссылок после просмотра {p} страницы - {len(list_result)}')
    return list_result


# if __name__ == '__main__':
    # main_foo()
    # find_news()
    # open_href()