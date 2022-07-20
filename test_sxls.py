from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
import pandas as pd
from main import main_foo

def excel():
    #df = pd.DataFrame({'№': [], 'Имя запроса': [], 'Дата': [], 'URL объявления': [], 'Описание': []})
    #df.to_excel('test_xlsx.xlsx', sheet_name='Statistic', index=False)

    list_result = main_foo()
    fn = 'test_xlsx.xlsx'
    wb = load_workbook(fn)
    ws = wb['Statistic']
    #ws.column_dimensions[get_column_letter(2)].width = 20
    #ws.column_dimensions[get_column_letter(3)].width = 20
    #ws.column_dimensions[get_column_letter(4)].width = 50
    #ws.column_dimensions[get_column_letter(5)].width = 50
    i = 2 # Ячейка, с которой начинается заполнения, НО НУЖНО ПРИДУМАТЬ КАК ОПРЕДЕЛИТЬ ПОСЛЕДНУЮЮ НЕЗАПОЛНЕННУЮ СТРОЧКУ
    for j in list_result:
        ws[f'A{i}'] = f'{i-1}'
        ws[f'B{i}'] = f'{j[0]}'
        ws[f'C{i}'] = f'{j[1]}'
        ws[f'D{i}'] = f'{j[2]}'
        ws[f'E{i}'] = f'{j[3]}'
        i += 1
    wb.save(fn)
    wb.close()

if __name__ == '__main__':
    excel()
