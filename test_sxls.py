from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
import pandas as pd
from main import main_foo

def excel():
    df = pd.DataFrame({'№': [], 'Имя запроса': [], 'Дата': [], 'URL объявления': [], 'Контакт': [], 'Описание': []})
    df.to_excel('test_xlsx.xlsx', sheet_name='Statistic', index=False)

    list_result = main_foo()
    fn = 'test_xlsx.xlsx'
    wb = load_workbook(fn)
    ws = wb['Statistic']
    ws.column_dimensions[get_column_letter(2)].width = 40
    ws.column_dimensions[get_column_letter(3)].width = 40
    ws.column_dimensions[get_column_letter(4)].width = 100
    ws.column_dimensions[get_column_letter(5)].width = 50
    ws.column_dimensions[get_column_letter(6)].width = 100
    for i, j in enumerate(list_result):
        ws[f'A{i + 2}'] = f'{i}'
        # ws[f'B{i + 2}'] = f'{i}' ПОД ВОПРОСОМ
        ws[f'C{i + 2}'] = f'{j[0]}'
        ws[f'D{i + 2}'] = f'{j[1]}'
        ws[f'E{i + 2}'] = f'{j[2]}'
        ws[f'F{i + 2}'] = f'{j[3]}'
    wb.save(fn)
    wb.close()

excel()