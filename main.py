from parser_class import SeleniumParser
from to_excel import get_rows, get_table


def main():
    solo_parsing = True # спарсить один бренд
    parser = SeleniumParser(sleep_time=2, solo_parsing=solo_parsing, save_html=False, headless=False)
    data, brand = parser.get_data()
    parser.close()
    rows = get_rows(data)
    if solo_parsing:
        get_table(rows, brand)
    else:
        get_table(rows)


if __name__ == '__main__':
    main()