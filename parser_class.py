import os
import time
import json
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class SeleniumParser:
    def __init__(self, save_html=False, sleep_time=3, solo_parsing=False, headless=True):
        self.headless = headless
        self.driver = self.__get_driver()
        self.save_html = save_html
        self.solo_parsing = solo_parsing
        self.sleep_time = sleep_time
    
    def __get_driver(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(
            # service='',
            options=options
        )
        return driver
    
    def __login(self):
        uname = '17812169682'
        upwd = 'InSha256Griz'
        self.driver.get('http://web.yilaitong.net/')
        self.driver.implicitly_wait(10)
        userinput = self.driver.find_element(By.ID, 'uname')
        userinput.send_keys(uname)
        pwdinput = self.driver.find_element(By.ID, 'upwd')
        pwdinput.send_keys(upwd)
        self.driver.implicitly_wait(10)
        pwdinput.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(10)

    def __open_tab(self):
        tab = self.driver.find_element(By.ID, 'BaojiaSelectModel')
        tab.click()
        self.driver.implicitly_wait(10)

    def __get_htmls(self, elems):
        res = []
        for elem in elems:
            res.append(f"{elem.get_attribute('outerHTML')}\n")
        return res

    def __save_elem_to_html(self, brand, model_one, model_two, htmls):
        if not os.path.exists('htmls'):
            os.mkdir('htmls')
        filename = f'htmls/{brand.replace('/', '-').replace('_', ' ')}_{model_one.replace('/', '-').replace('_', ' ')}_{model_two.replace('/', '-').replace('_', ' ')}.html'
        with open(filename, 'w', encoding='utf8') as file:
            file.writelines(htmls)

    def __get_webelems(self, brand_name, brand_counter=0, brand_lenght=0):
        webelems = []
        model_one_select_elem = self.driver.find_element(By.CLASS_NAME, 'bb')
        model_one_select = Select(model_one_select_elem)
        model_one_options = model_one_select.options
        first_time_model_one = True
        l1 = len(model_one_options)
        for j in range(1, l1):
            if self.solo_parsing:
                print(f'params 1: {j}/{l1 - 1}', end='\r')
            else:
                print(f'brands: {brand_counter}/{brand_lenght - 1} | params 1: {j}/{l1 - 1}', end='\r')
            if first_time_model_one == False:
                l1_check = 0
                counter = 0
                while l1_check != l1:
                    if counter > 0 and counter < 3:
                        time.sleep(0.5)
                    elif counter > 3:
                        break
                    counter += 1
                    model_one_select_elem = self.driver.find_element(By.CLASS_NAME, 'bb')
                    model_one_select = Select(model_one_select_elem)
                    l1_check = len(model_one_select.options)
            else:
                first_time_model_one = False
            try:
                model_one_option = model_one_select.options[j]
            except:
                continue
            model_one_value = model_one_option.get_attribute('value')
            model_one_name = model_one_option.text
            model_one_select.select_by_value(model_one_value)
            # driver.implicitly_wait(10)
            time.sleep(self.sleep_time)
            # set model 2
            model_two_select_elem = self.driver.find_element(By.CLASS_NAME, 'cc')
            model_two_select = Select(model_two_select_elem)
            model_two_options = model_two_select.options
            first_time_model_two = True
            l2 = len(model_two_options)
            for k in range(1, l2):
                if self.solo_parsing:
                    print(f'params 1: {j}/{l1 - 1} | params 2: {k}/{l2 - 1}', end='\r')
                else:
                    print(f'brands: {brand_counter}/{brand_lenght - 1} | params 1: {j}/{l1 - 1} | params 2: {k}/{l2-1}', end='\r')
                if first_time_model_two == False:
                    l2_check = 0
                    counter = 0
                    while l2_check != l2:
                        if counter > 0 and counter < 3:
                            time.sleep(0.5)
                        elif counter > 3:
                            break
                        counter += 1
                        model_two_select_elem = self.driver.find_element(By.CLASS_NAME, 'cc')
                        model_two_select = Select(model_two_select_elem)
                        l2_check = len(model_two_select.options)
                else:
                    first_time_model_two = False
                try:
                    model_two_option = model_two_select.options[k]
                except:
                    continue
                model_two_value = model_two_option.get_attribute('value')
                model_two_name = model_two_option.text
                model_two_select.select_by_value(model_two_value)
                # driver.implicitly_wait(10)
                time.sleep(self.sleep_time)
                # press search
                search_button = self.driver.find_element(By.CLASS_NAME, 'sou')
                search_button.click()
                self.driver.implicitly_wait(10)
                time.sleep(self.sleep_time)
                # save page
                data_div = self.driver.find_elements(By.CLASS_NAME, 'row')
                htmls = self.__get_htmls(data_div)
                if self.save_html:
                    self.__save_elem_to_html(brand_name, model_one_name, model_two_name, htmls)
                webelems.append([brand_name, model_one_name, model_two_name, htmls])
        return webelems

    def __get_elems(self):
        elems = []
        brand_name = ''
        select_bar = self.driver.find_element(By.CLASS_NAME, 'check')
        city_select_elem = select_bar.find_element(By.CLASS_NAME, 'cityList')
        city_select = Select(city_select_elem)
        city_options = city_select.options
        all_citites = city_options[-1].get_attribute('value')
        city_select.select_by_value(all_citites)
        # set brand
        brand_select_elem = select_bar.find_element(By.CLASS_NAME, 'aa')
        brand_select = Select(brand_select_elem)
        brand_options = brand_select.options
        first_time = True

        if self.solo_parsing:
            print('Бренды:')
            for i, brand_option in enumerate(brand_options[1:]):
                print(f'{i + 1}. {brand_option.text}')
            brand_id = int(input('Введите id бренда: '))
            brand_value = brand_options[brand_id].get_attribute('value')
            brand_name = brand_options[brand_id].text
            brand_select.select_by_value(brand_value)
            time.sleep(self.sleep_time)
            webelems = self.__get_webelems(brand_name)
            elems.extend(webelems)
        else:
            l_brands = len(brand_options)
            for i in range(1, l_brands):
                print(f'brands: {i}/{l_brands - 1}', end='\r')
                if first_time == False:
                    l_check = 0
                    counter = 0
                    while l_check != l_brands:
                        brand_select_elem = self.driver.find_element(By.CLASS_NAME, 'aa')
                        brand_select = Select(brand_select_elem)
                        l_check = len(brand_select.options)
                        if counter > 0 and counter < 3:
                            time.sleep(0.5)
                        elif counter > 3:
                            break
                        counter += 1
                else:
                    first_time = False
                try:
                    brand_option = brand_select.options[i]
                except:
                    continue
                brand_value = brand_option.get_attribute('value')
                brand_name = brand_option.text
                brand_select.select_by_value(brand_value)
                # driver.implicitly_wait(10)
                time.sleep(self.sleep_time)
                webelems = self.__get_webelems(brand_name, brand_counter=i, brand_lenght=len(brand_options)-1)
                elems.extend(webelems)
        return elems, brand_name
    
    def get_data(self):
        self.__login()
        self.__open_tab()
        data_htmls = self.__get_elems()
        return data_htmls   

    def close(self):
        self.driver.quit()

def main():
    parser = SeleniumParser(save_html=True, sleep_time=2)
    parser.get_data()

if __name__ == '__main__':
    main()