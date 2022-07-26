from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
import pandas as pd
from main import main_foo, find_news


def excel_news(period, *args):
    # df = pd.DataFrame({'№': [], 'Имя запроса': [], 'Дата': [], 'URL объявления': [], 'Описание': []})
    # df.to_excel('test_xlsx.xlsx', sheet_name='Statistic', index=False)

    if period == 'm':
        list_result = find_news('m')
    else:
        list_result = find_news('p', *args)
    fn = 'test_news.xlsx'
    wb = load_workbook(fn)
    ws = wb['Statistic']
    # ws.column_dimensions[get_column_letter(2)].width = 20
    # ws.column_dimensions[get_column_letter(3)].width = 20
    # ws.column_dimensions[get_column_letter(4)].width = 50
    # ws.column_dimensions[get_column_letter(5)].width = 50
    i = 2  # Ячейка, с которой начинается заполнения, НО НУЖНО ПРИДУМАТЬ КАК ОПРЕДЕЛИТЬ ПОСЛЕДНУЮЮ НЕЗАПОЛНЕННУЮ СТРОЧКУ
    for j in list_result:
        ws[f'A{i}'] = f'{i - 1}'
        ws[f'B{i}'] = f'{j[0]}'
        ws[f'C{i}'] = f'{j[1]}'
        ws[f'D{i}'] = f'{j[2]}'
        ws[f'E{i}'] = f'{j[3]}'
        i += 1
    wb.save(fn)
    wb.close()


def excel():
    #df = pd.DataFrame({'№': [], 'Имя запроса': [], 'Дата': [], 'URL объявления': [], 'Описание': []})
    #df.to_excel('test_xlsx.xlsx', sheet_name='Statistic', index=False)

    list_result = main_foo()
    fn = 'test_xlsx.xlsx'
    wb = load_workbook(fn)
    ws = wb['Statistic']
    row = ws.max_row + 1
    #ws.column_dimensions[get_column_letter(2)].width = 20
    #ws.column_dimensions[get_column_letter(3)].width = 20
    #ws.column_dimensions[get_column_letter(4)].width = 50
    #ws.column_dimensions[get_column_letter(5)].width = 50
    count = True
    # Ячейка, с которой начинается заполнения, НО НУЖНО ПРИДУМАТЬ КАК ОПРЕДЕЛИТЬ ПОСЛЕДНУЮЮ НЕЗАПОЛНЕННУЮ СТРОЧКУ
    for j in list_result:
        for i in ws['D']:
            if j[2] == i.value:
                count = False
                break
        if count:
            ws[f'A{row}'] = f'{row - 1}'
            ws[f'B{row}'] = f'{j[0]}'
            ws[f'C{row}'] = f'{j[1]}'
            ws[f'D{row}'] = j[2]
            ws[f'E{row}'] = f'{j[3]}'
            row += 1
    wb.save(fn)
    wb.close()

if __name__ == '__main__':
    # excel()
    excel_news('p', '1/1/2020', '3/3/2020')
