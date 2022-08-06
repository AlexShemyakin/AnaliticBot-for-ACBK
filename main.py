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

    list_result = []
    count_requests = 0
    count_pages = 0
    firefox_options = Options()
    firefox_options.add_argument('user-data-dir=selenium')
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
    driver.get('https://google.com/')

    for req in list_key:
        if count_requests == 1:
            search = driver.find_element(by=By.XPATH,
                                         value='/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/div/div[2]/input')
        else:
            search = driver.find_element(by=By.XPATH,
                                         value='/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')

        search.clear()
        search.send_keys(req)
        search.submit()
        time.sleep(1)

        if period == 'm' and count_requests == 0:
            driver.find_element(by=By.CLASS_NAME, value='t2vtad').click()
            driver.find_elements(by=By.CLASS_NAME, value='KTBKoe')[1].click()
            driver.find_elements(by=By.CLASS_NAME, value='tnhqA')[12].click()
            count_requests = 1

        elif period == 'p' and count_requests == 0:
            driver.find_element(by=By.CLASS_NAME, value='t2vtad').click()
            driver.find_elements(by=By.CLASS_NAME, value='KTBKoe')[1].click()
            driver.find_elements(by=By.CLASS_NAME, value='tnhqA')[14].click()
            driver.find_element(by=By.ID, value='OouJcb').send_keys(args[0])
            driver.find_element(by=By.ID, value='rzG2be').send_keys(args[1])
            driver.find_elements(by=By.CLASS_NAME, value='fE5Rge')[0].click()
            count_requests = 1

        while count_pages < 2:
            #Поиск заголовков и ссылок
            try:
                search = driver.find_elements(by=By.CLASS_NAME, value='jGGQ5e')
            except:
                break
            for j, i in enumerate(search):
                list_attr = []
                header = i.text.find('\n')
                header = i.text[:header]

                href = driver.find_element(by=By.PARTIAL_LINK_TEXT, value=header)
                href = href.get_attribute('href')

                try:
                    date = driver.find_elements(by=By.CLASS_NAME, value='WZ8Tjf')
                except:
                    break
                if re.search(r'час', f'{date[j].text}'):
                    date_public = datetime.today().strftime('%Y.%m.%d')
                elif re.search(r'дне', f'{date[j].text}') or re.search(r'дня', f'{date[j].text}') or\
                        re.search(r'ден', f'{date[j].text}'):
                    space = date[j].text.find(' ')
                    date_public = datetime.today() - timedelta(days=int(date[j].text[:space]))
                    date_public = date_public.strftime('%Y.%m.%d')
                elif re.search(r'г.', f'{date[j].text}'):
                    d_m_y = date[j].text.split(' ')
                    day = d_m_y[0]
                    month = d_m_y[1]
                    year = d_m_y[2]
                    if re.search(r'янв', month):
                        month = '01'
                    elif re.search(r'фев', month):
                        month = '02'
                    elif re.search(r'мар', month):
                        month = '03'
                    elif re.search(r'апр', month):
                        month = '04'
                    elif re.search(r'ма', month):
                        month = '05'
                    elif re.search(r'июн', month):
                        month = '06'
                    elif re.search(r'июл', month):
                        month = '07'
                    elif re.search(r'авг', month):
                        month = '08'
                    elif re.search(r'сен', month):
                        month = '09'
                    elif re.search(r'окт', month):
                        month = '10'
                    elif re.search(r'ноя', month):
                        month = '11'
                    elif re.search(r'дек', month):
                        month = '12'


                    date_public = datetime(int(year), int(month), int(day))
                    date_public = date_public.strftime('%Y.%m.%d')

                else:
                    date_public = '0.0.0'

                list_attr.append(req)
                list_attr.append(date_public)
                list_attr.append(href)
                list_attr.append(header)
                list_result.append(list_attr)

            try:
                search = driver.find_element(by=By.PARTIAL_LINK_TEXT, value='Следующая')
                count_pages += 1
            except:
                break
            search.click()

    driver.close()
    # list_result = sorted(list_result, key=itemgetter(0, 1, 2), reverse=True)
    return list_result



def open_href(href, request):
    url = f'{href}'
    page = requests.get(url)  # извлекаем данные в переменную
    soup = BeautifulSoup(page.text, 'html.parser')  # сохраняем html страницы, откуда будем извлекать данные
    description = soup.find('div', {'class': 'css-g5mtbi-Text'}).get_text()
    date_public = soup.find('span', {'class': 'css-19yf5ek'}).get_text()

    # Если объявление было выложено в этот день с надписью "Сегодня" ты форматируем в привычный формат
    if re.search('Сегодня', f'{date_public}'):
        date_public = datetime.today().strftime('%Y.%m.%d')
    else:
        d_m_y = date_public.split(' ')
        day = d_m_y[0]
        month = d_m_y[1]
        year = d_m_y[2]
        if re.search(r'янв', month):
            month = '01'
        elif re.search(r'фев', month):
            month = '02'
        elif re.search(r'мар', month):
            month = '03'
        elif re.search(r'апр', month):
            month = '04'
        elif re.search(r'ма', month):
            month = '05'
        elif re.search(r'июн', month):
            month = '06'
        elif re.search(r'июл', month):
            month = '07'
        elif re.search(r'авг', month):
            month = '08'
        elif re.search(r'сен', month):
            month = '09'
        elif re.search(r'окт', month):
            month = '10'
        elif re.search(r'ноя', month):
            month = '11'
        elif re.search(r'дек', month):
            month = '12'

        date_public = datetime(int(year), int(month), int(day))
        date_public = date_public.strftime('%Y.%m.%d')


    return [request, date_public, href, description]


def main_foo():
    #list of requests
    list_of_requests = ['рога сайгака', 'степная черепаха',
                        'среднеазиатская черепаха', 'живая черепаха', 'продам черепаху']
    #
    # list_of_requests = ['рога сайгака']
    # list of result data
    list_result = []

    # ПЕРЕБОР ЗАПРОСОВ ИЗ list_of_requests
    for i in list_of_requests:
        url_olx = f'https://www.olx.kz/list/q-{i}/'
        page = requests.get(url_olx) #извлекаем данные в переменную
        soup = BeautifulSoup(page.text, 'html.parser') #сохраняем html страницы, откуда будем извлекать данные
        pages = len(soup.findAll('li', {"class": "brmwmy"})) #кол-во страниц, доступных для перелистывания
        # s = soup.find_all('h3')
        # if re.search(r'Мы нашли 0', f"{soup.find_all('div')[0].get_text()}"):
        #     print('Не найдено объявлений')
        #     continue
        # if re.search(r'Топ', f"{soup.find_all('h2')[0].get_text()}"):
        #     print(f"По запросу '{i}' {soup.find_all('h3')[0].get_text()}")
        # else:
        #     print(f"По запросу '{i}' {soup.find_all('h3')[0].get_text()}")
        #
        # # if re.search(r'Не найдено', f"{soup.find_all('p')[3].get_text()}"):
        #     print('Не найдено объявлений')
        #     continue
        # if re.search(r'Топ', f"{soup.find_all('h2')[0].get_text()}"):
        #     print(f"По запросу '{i}' {soup.find_all('p')[7].get_text()}")
        # else:
        #     print(f"По запросу '{i}' {soup.find_all('h2')[1].get_text()}")


        #Если всего одна страница, то присвоем ей номер 1, чтобы цикл for начался
        if pages == 0:
            pages = 1

        for p in range(1, pages+1): #перебор всех страниц по запросу
            url_olx = f'https://www.olx.kz/d/list/q-{i}/?page={p}'
            page = requests.get(url_olx)
            soup = BeautifulSoup(page.text, 'html.parser')

            # Кол-во объявлений на каждой странице
            list_of_ads = soup.find_all('a', {'class': 'css-1bbgabe'})

            # Перебор всех объявлений со страницы и достаем от туда href
            for ad in list_of_ads:

                # Если этого объявления еще нет в list_href, то добавляем
                if ad.__getattribute__('attrs')['href'] not in list_result:
                    href = f"https://olx.kz{ad.__getattribute__('attrs')['href']}"
                    list_result.append(open_href(href, i))
            # list_result = sorted(list_result, key=itemgetter(0, 1), reverse=True)
            # print(f'Кол-во ссылок после просмотра {p} страницы - {len(list_result)}')
    return list_result


if __name__ == '__main__':
    # main_foo()
    find_news('p', '1.1.2021', '31.5.2021')
    # find_news('m')
    # open_href()
