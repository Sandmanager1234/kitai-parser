import os
import json
import datetime
import pandas as pd
from bs4 import BeautifulSoup

def get_pages():
    result = []
    l = os.listdir('htmls')
    for html in l:
        brand, model_one, model_two = html.replace('.html', '').split('_')
        with open(f'htmls/{html}', 'r', encoding='utf8') as file:
            data = file.readlines()
        result.append([brand, model_one, model_two, data])
    return result

def get_rows(elems):
    rows = []
    for elem in elems:
        # print(len(elem[3]))
        for sku in elem[3]:
            row = {
                'Param 1': elem[0],
                'Param 2': elem[1],
                'Param 3': elem[2]
            }
            soup = BeautifulSoup(sku, 'lxml')
            sku_name = soup.find('div', class_='case bg').text
            # print(sku_name)
            row['Model (sku)'] = sku_name
            # soup.con
            details = soup.find_all('div')[1:]
            for i, detail in enumerate(details):
                conts = detail.contents
                if len(conts) > 2:
                    price = conts[0]
                    text = conts[5]
                    value = f'{price} ({text})'
                else:
                    value = ''
                row[f'details_{i+1}'] = value
            rows.append(row)
    return rows

def get_table(rows, brand_name=''):
    df = pd.DataFrame(rows)
    if brand_name == '':
        filename = f'import_{datetime.datetime.today().strftime("%d-%m-%Y")}.xlsx'
    else:
        filename = f'{brand_name}_import_{datetime.datetime.today().strftime("%d-%m-%Y")}.xlsx'
    df.to_excel(filename, index=False)

def main():
    htmls = get_pages()
    rows = get_rows(htmls)
    get_table(rows)
    # with open('rows.json', 'w', encoding='utf8') as file:
    #     json.dump(rows, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()