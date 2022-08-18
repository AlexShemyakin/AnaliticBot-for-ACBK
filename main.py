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


def find_month(month):
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
    else:
        month = ' '

    return month


#поиск новостей
def find_news(period, *args):
    list_key = ['контрабанда рогов сайгака', 'контрабанда сайгачьих рогов', 'незаконный вывоз рогов сайгака',
                'контрабандный вывоз степных черепах', 'незаконный вывоз балобанов']

    list_result = []
    count_requests = 0
    count_pages = 0
    firefox_options = Options()
    firefox_options.add_argument('user-data-dir=selenium')
    # firefox_options.add_argument("--headless")
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

                    month = find_month(month)

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
    return list_result


#открытие объявлений с olx.kz
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

        month = find_month(month)

        date_public = datetime(int(year), int(month), int(day))
        date_public = date_public.strftime('%Y.%m.%d')

    return [request, date_public, href, description]


#поиск на olx
def pars_olx():
    #list of requests
    list_of_requests = ['рога сайгака', 'степная черепаха',
                        'среднеазиатская черепаха', 'живая черепаха', 'продам черепаху']

    # list of result data
    list_result = []

    # ПЕРЕБОР ЗАПРОСОВ ИЗ list_of_requests
    for i in list_of_requests:
        url_olx = f'https://www.olx.kz/d/list/q-{i}/'

        # извлекаем данные в переменную
        page = requests.get(url_olx)

        # сохраняем html страницы, откуда будем извлекать данные
        soup = BeautifulSoup(page.text, 'html.parser')

        # кол-во страниц, доступных для перелистывания
        pages = len(soup.find_all('a', {'class': 'css-1mi714g'}))

        # pages = len(soup.findAll('li', {"class": "brmwmy"}))

        #Если всего одна страница, то присвоем ей номер 1, чтобы цикл for начался
        if not pages:   pages = 1
        else:   pages = int(soup.find_all('a', {'class': 'css-1mi714g'})[-1].get_text())

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
    return list_result


#открытие объявлений с edc.kz
def open_href_edc(href, request):
    url = f'{href}'
    page = requests.get(url)  # извлекаем данные в переменную
    soup = BeautifulSoup(page.text, 'html.parser')  # сохраняем html страницы, откуда будем извлекать данные
    description = soup.find('div', {'class': 'c-article'}).get_text()
    date_public = soup.find('span', {'class': 'nowrap'}).get_text()


    d_m_y = date_public.split(' ')
    day = d_m_y[2]
    month = d_m_y[3]
    if len(d_m_y) == 4:
        year = datetime.today().year
    else:
        year = d_m_y[5]

    month = find_month(month)

    date_public = datetime(int(year), int(month), int(day))
    date_public = date_public.strftime('%Y.%m.%d')

    return [request, date_public, href, description]


#поиск на edc.kz
def pars_edc():
    #list of requests
    list_of_requests = ['рога сайгака', 'степная черепаха',
                        'среднеазиатская черепаха', 'живая черепаха', 'продам черепаху']
    #
    # list_of_requests = ['рога сайгака']

    # list of result data
    list_result = []

    # ПЕРЕБОР ЗАПРОСОВ ИЗ list_of_requests
    for i in list_of_requests:
        url = f'https://edc.sale/ru/kz/search/?ct=0&lt=&fa=0&sort=&cur=&' \
                  f'page=1&q={i}'

        # извлекаем данные в переменную
        page = requests.get(url)

        # сохраняем html страницы, откуда будем извлекать данные
        soup = BeautifulSoup(page.text, 'html.parser')

        # кол-во страниц, доступных для перелистывания
        pages = len(soup.findAll('li', {"class": "page-item"}))

        #Если всего одна страница, то присвоем ей номер 1, чтобы цикл for начался
        if pages == 0:
            pages = 1

        for p in range(1, pages+1): #перебор всех страниц по запросу
            url = f'https://edc.sale/ru/kz/search/?ct=0&lt=&fa=0&sort=&cur=&' \
                  f'page={p}&q={i}'
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            # Кол-во объявлений на каждой странице
            list_of_ads = soup.findAll('div', {'class': 'it-grid-item-in'})
            # if not list_of_ads:
            #     break
            # Перебор всех объявлений со страницы и достаем от туда href
            for ad in list_of_ads:
                href = ad.__getattribute__('contents')[1]
                href = href.__getattribute__('attrs')['href']
                # Если этого объявления еще нет в list_href, то добавляем
                if href not in list_result:
                    href = f"https://edc.sale/ru/{href}"
                    list_result.append(open_href_edc(href, i))
    return list_result


#поиск на market.kz
def pars_market():
    #list of requests
    list_of_requests = ['рога сайгака', 'степная черепаха',
                        'среднеазиатская черепаха', 'живая черепаха', 'продам черепаху']

    # list of result data
    list_result = []

    # ПЕРЕБОР ЗАПРОСОВ ИЗ list_of_requests
    for i in list_of_requests:
        url = f'https://market.kz/k--{i}'

        # извлекаем данные в переменную
        page = requests.get(url)

        # сохраняем html страницы, откуда будем извлекать данные
        soup = BeautifulSoup(page.text, 'html.parser')

        # кол-во страниц, доступных для перелистывания
        pages = len(soup.findAll('div', {"class": "pagination"}))
        if pages:
            pages = soup.find('div', {"class": "pagination"}).__getattribute__('contents')
            pages = len(pages[0].__getattribute__('contents'))
        else:
            pages = 1

        for p in range(1, pages+1): #перебор всех страниц по запросу
            url = f'https://market.kz/k--{i}/?page={p}'
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            # Кол-во объявлений на каждой странице
            list_of_ads = soup.findAll('div', {'class': 'a-card__content'})

            # Перебор всех объявлений со страницы и достаем от туда href
            for ad in list_of_ads:
                temp = ad.__getattribute__('contents')[1]
                temp = temp.__getattribute__('contents')[1]

                href = temp.__getattribute__('attrs')['href']

                desrciption = temp.__getattribute__('contents')[1]
                desrciption = desrciption.__getattribute__('attrs')['alt']

                date_public = soup.find('div', {'class': "card-stats"}).__getattribute__('contents')[3]
                date_public = date_public.__getattribute__('contents')[1]
                date_public = date_public.__getattribute__('contents')[0]

                d_m_y = date_public.split(' ')
                day = d_m_y[0]
                month = d_m_y[1]
                year = d_m_y[2]

                month = find_month(month)

                date_public = datetime(int(year), int(month), int(day))
                date_public = date_public.strftime('%Y.%m.%d')

                temp_list = [i, date_public, href, desrciption]
                print(temp_list)
                list_result.append(temp_list)
    return list_result


#поиск на salaxy.kz
def pars_salaxy():
    #list of requests
    list_of_requests = ['рога сайгака', 'степная черепаха',
                        'среднеазиатская черепаха', 'живая черепаха', 'черепаху']

    # list of result data
    list_result = []

    # ПЕРЕБОР ЗАПРОСОВ ИЗ list_of_requests
    for i in list_of_requests:
        url = f'https://salexy.kz/all?Filter%5Bdistrict_id%5D=&Filter%5Bsearch_string%5D={i}'

        # извлекаем данные в переменную
        page = requests.get(url)

        # сохраняем html страницы, откуда будем извлекать данные
        soup = BeautifulSoup(page.text, 'html.parser')

        # кол-во страниц, доступных для перелистывания
        pages = len(soup.findAll('li', {"class": "page"}))
        if not pages:
            pages = 1

        for p in range(1, pages+1): #перебор всех страниц по запросу
            url = f'https://salexy.kz/all?Filter%5Bdistrict_id%5D=&Filter%5Bsearch_string%5D={i}#page={p}'
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            #Флаг, определяющий кол-во объявлений до лишних объявлений с другого города
            flag = soup.find('ul', {'class': 'product-list'})
            flag = flag.__getattribute__('contents')

            for ad in flag:
                if ad == '\n':
                    continue
                elif ad.text.isspace():
                    continue
                elif re.search('соседн', ad.text):
                    break

                temp = ad.__getattribute__('contents')[3]
                temp = temp.__getattribute__('contents')[1]
                temp = temp.__getattribute__('contents')[1]

                desrciption = temp.__getattribute__('contents')[1].text

                href = temp.__getattribute__('contents')[1]
                href = href.__getattribute__('contents')[0]
                href = href.__getattribute__('attrs')['href']

                date_public = temp.__getattribute__('contents')[7]
                try:
                    date_public = date_public.__getattribute__('contents')[1].text
                    d_m_y = date_public.split('.')
                    day = d_m_y[0]
                    month = d_m_y[1]
                    year = d_m_y[2]

                    date_public = datetime(int(year), int(month), int(day))
                    date_public = date_public.strftime('%Y.%m.%d')
                except IndexError:
                    date_public = ''


                temp_list = [i, date_public, href, desrciption]
                list_result.append(temp_list)
                print(temp_list)

    return list_result


#поиск на slanet.kz
def pars_slanet():
    #list of requests
    list_of_requests = ['рога сайгака', 'степная черепаха',
                        'среднеазиатская черепаха', 'живая черепаха', 'черепаха']

    # list of result data
    list_result = []

    # ПЕРЕБОР ЗАПРОСОВ ИЗ list_of_requests
    for i in list_of_requests:
        url = f'https://slanet.kz/index.php?page=search&sOrder=dt_pub_date&iOrderType=desc&sPattern={i}'

        # извлекаем данные в переменную
        page = requests.get(url)

        # сохраняем html страницы, откуда будем извлекать данные
        soup = BeautifulSoup(page.text, 'html.parser')

        # кол-во страниц, доступных для перелистывания
        pages = soup.find_all('a', {'class': "list-last"})
        if pages:
            pages = pages[0].__getattribute__('attrs')['href']
            pages = int(pages[-1:])
        else:
            pages = len(soup.find_all('a', {'class': "searchPaginationNonSelected"}))
            if not pages:
                pages = 1

        for p in range(1, pages+1): #перебор всех страниц по запросу
            url = f'https://slanet.kz/index.php?page=search&sOrder=dt_pub_date&iOrderType=desc&sPattern={i}&iPage={p}'
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            # Объявления на каждой странице
            list_of_ads = soup.findAll('div', {'class': 'grid'})
            if not list_of_ads:
                 break

            # Перебор всех объявлений со страницы и достаем от туда href
            for ad in list_of_ads[0].__getattribute__('contents'):
                if ad == '\n':
                    continue
                elif ad == ' ':
                    continue

                #Определение общего html
                temp = ad.__getattribute__('contents')[1]
                temp = temp.__getattribute__('contents')[1]

                #Выделение href
                href = temp.__getattribute__('contents')[1]
                href = href.__getattribute__('attrs')['href']

                #Выделение даты
                date_public = temp.__getattribute__('contents')[3]
                date_public = date_public.__getattribute__('text')
                date_public = date_public.split(' ')
                count = date_public[0]

                if re.search('нед', date_public[1]):
                    date_public = datetime.today() - timedelta(weeks=int(count))
                elif re.search('месяц', date_public[1]):
                    date_public = datetime.today() - timedelta(weeks=int(count) * 4)
                elif re.search('час', date_public[1]):
                    date_public = datetime.today() - timedelta(hours=int(count))
                else:
                    date_public = ''
                date_public = date_public.strftime('%Y.%m.%d')

                # Выделение описания
                desrciption = temp.__getattribute__('contents')[1]
                desrciption = desrciption.__getattribute__('contents')[0]
                desrciption = desrciption.__getattribute__('attrs')['alt']

                temp_list = [i, date_public, href, desrciption]
                list_result.append(temp_list)

                print(temp_list)
                print('\n')
    return list_result


#поиск на avi.kz
def pars_avi():
    #list of requests
    list_of_requests = ['рога сайгака', 'степная черепаха',
                        'среднеазиатская черепаха', 'живая черепаха']

    # list of result data
    list_result = []

    # ПЕРЕБОР ЗАПРОСОВ ИЗ list_of_requests
    for i in list_of_requests:
        url = f'https://avi.kz/search/?ct=0&lt=0&sort=&page=1&q={i}'

        # извлекаем данные в переменную
        page = requests.get(url)

        # сохраняем html страницы, откуда будем извлекать данные
        soup = BeautifulSoup(page.text, 'html.parser')

        # кол-во страниц, доступных для перелистывания
        pages = len(soup.find_all('a', {'class': "j-pgn-page"}))
        if pages < 3:
            pages = 2
        elif pages >= 3:
            pages = pages - 1
        else:
            pages = 1

        # перебор всех страниц по запросу
        for p in range(1, pages+1):
            url = f'https://avi.kz/search/?ct=0&lt=0&sort=&page={p}&q={i}'
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            # Объявления на каждой странице
            list_of_ads = soup.find_all('div', {'class': 'sr-2-list-item-n-body'})

            # Перебор всех объявлений со страницы и достаем от туда href
            for ad in list_of_ads:

                #Выделение href
                href = ad.__getattribute__('contents')[3]
                href = href.__getattribute__('contents')[1]
                href = href.__getattribute__('attrs')['href']

                #Выделение даты
                try:
                    date_public = ad.__getattribute__('contents')[7]
                except:
                    date_public = ad.__getattribute__('contents')[5]
                date_public = date_public.__getattribute__('contents')[3].text
                date_public = date_public.split(' ')

                if len(date_public) == 2:
                    year = datetime.today().year
                    day = date_public[0]
                    month = date_public[1]

                    month = find_month(month)

                    date_public = datetime(int(year), int(month), int(day))

                elif len(date_public) == 1:
                    temp = date_public[0]
                    if re.search('Сегодн', temp):
                        date_public = datetime.today()
                    elif re.search('Вчера', temp):
                        date_public = datetime.today() - timedelta(days=1)

                elif len(date_public) == 3:
                    day = date_public[0]
                    month = date_public[1]
                    year = date_public[2]

                    month = find_month(month)

                    date_public = datetime(int(year), int(month), int(day))

                date_public = date_public.strftime('%Y.%m.%d')

                # Выделение описания
                desrciption = ad.__getattribute__('contents')[3]
                desrciption = desrciption.__getattribute__('contents')[1].text

                temp_list = [i, date_public, href, desrciption]
                list_result.append(temp_list)

                print(temp_list)
                print('\n')
    return list_result


if __name__ == '__main__':
    # edc_sale()
    # pars_olx()
    # pars_slanet()
    # pars_salaxy()
    # pars_market()
    # find_news('p', '1.1.2021', '31.5.2021')
    pars_avi()
    # find_news('m')
    # open_href()
