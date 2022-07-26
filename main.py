import os
import time
from datetime import datetime, timedelta
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import re
from operator import itemgetter



def find_news(period, *args):
    list_key = ['контрабанда рогов сайгака', 'контрабанда сайгачьих рогов', 'незаконный вывоз рогов сайгака',
                'контрабандный вывоз степных черепах', 'незаконный вывоз балобанов']

    list_headers = []
    list_date = []
    list_href = []
    list_keyword = []
    count_requsts = 0
    firefox_options = Options()
    firefox_options.add_argument('user-data-dir=selenium')
    # firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
    driver.get('https://google.com/')

    for req in list_key:
        list_keyword.append(req)
        if count_requsts == 1:
            search = driver.find_element(by=By.XPATH,
                                         value='/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/div/div[2]/input')
        else:
            search = driver.find_element(by=By.XPATH,
                                         value='/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')

        search.clear()
        search.send_keys(req)
        search.submit()
        time.sleep(1)

        if period == 'm' and count_requsts == 0:
            driver.find_element(by=By.CLASS_NAME, value='t2vtad').click()
            driver.find_elements(by=By.CLASS_NAME, value='KTBKoe')[1].click()
            driver.find_elements(by=By.CLASS_NAME, value='tnhqA')[12].click()
            count_requsts = 1

        elif period == 'p' and count_requsts == 0:
            driver.find_element(by=By.CLASS_NAME, value='t2vtad').click()
            driver.find_elements(by=By.CLASS_NAME, value='KTBKoe')[1].click()
            driver.find_elements(by=By.CLASS_NAME, value='tnhqA')[14].click()
            driver.find_element(by=By.ID, value='OouJcb').send_keys(args[0])
            driver.find_element(by=By.ID, value='rzG2be').send_keys(args[1])
            driver.find_elements(by=By.CLASS_NAME, value='fE5Rge')[0].click()
            count_requsts = 1


        #Поиск заголовков и ссылок
        search = driver.find_elements(by=By.CLASS_NAME, value='yuRUbf')
        for i in search:
            header = i.text.find('\n')
            header = i.text[:header]
            href = driver.find_element(by=By.PARTIAL_LINK_TEXT, value=header)
            href = href.get_attribute('href')
            list_href.append(href)
            list_headers.append(header)

        #Поиск дат
        date = driver.find_elements(by=By.CLASS_NAME, value='WZ8Tjf')
        for i in date:
            if re.search(r'час', f'{i.text}'):
                date = datetime.today().strftime('%d %B %Y г.')
            elif re.search(r'дне', f'{i.text}') or re.search(r'дня', f'{i.text}') or re.search(r'ден', f'{i.text}'):
                space = i.text.find(' ')
                date = datetime.today() - timedelta(days=int(i.text[:space]))
                date = date.strftime('%d %B %Y г.')
            elif re.search(r'г.', f'{i.text}'):
                date = i.text.find('г.')
                date = i.text[:date + 2]
            else:
                date = 'б/д'

            list_date.append(date)

    driver.close()
    print(list_keyword)
    print(list_date)
    print(list_keyword)
    print(list_href)

    return [list_keyword, list_date, list_keyword, list_href]



def open_href(href, request):
    url = f'{href}'
    page = requests.get(url)  # извлекаем данные в переменную
    soup = BeautifulSoup(page.text, 'html.parser')  # сохраняем html страницы, откуда будем извлекать данные
    description = soup.find('div', {'class': 'css-g5mtbi-Text'}).get_text()
    date_public = soup.find('span', {'class': 'css-19yf5ek'}).get_text()

    #Если объявление было выложено в этот день с надписью "Сегодня" ты форматируем в привычный формат
    if re.search(r'Сегодня', f"{date_public}"):
        date_public = datetime.today().strftime('%d %B %Y г.')
    return [request, date_public, href, description]


def main_foo():
    #list of requests
    list_of_requests = ['рога сайгака', 'степная черепаха',
                        'среднеазиатская черепаха', 'живая черепаха', 'продам черепаху']

    #list of result data
    list_result = []

    # ПЕРЕБОР ЗАПРОСОВ ИЗ list_of_requests
    for i in list_of_requests:
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
            # Кол-во объявлений на каждой странице
            list_of_ads = soup.findAll('a', {"class": "thumb"})
            # Перебор всех объявлений со страницы и достаем от туда href
            for ad in list_of_ads:
                # Если этого объявления еще нет в list_href, то добавляем
                if ad.__getattribute__('attrs')['href'] not in list_result:
                    href = ad.__getattribute__('attrs')['href']
                    list_result.append(open_href(href, i))
            list_result = sorted(list_result, key=itemgetter(0, 1), reverse=True)
            print(f'Кол-во ссылок после просмотра {p} страницы - {len(list_result)}')
    return list_result


if __name__ == '__main__':
    # main_foo()
    find_news(0, '1.1.2020', '2.2.2020')
    # open_href()