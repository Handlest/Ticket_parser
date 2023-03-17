import datetime
import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from useful_funcs import form_dictionary, show_ticket_dict, get_date_for_url, generate_graph_from_dict

# from_city = input("Пожалуйста, введите название города вылета в авиаформате (MOW - Москва, TOF - Томск)").upper()
# to_city = input("Пожалуйста, введите название города назначения в авиаформате (MOW - Москва, TOF - Томск)").upper()

from_city = "TOF"
to_city = "UUD"

exclude_list = ('Багаж', from_city, 'S7', to_city, '|', '+', 'Самый', 'Выбрать', 'цене', 'Без', 'Ред')


def parse_to_files(url, result_file):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")  # Disable web-driver mode
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                         " Chrome/96.0.4664.110 Safari/537.36")
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()), service_log_path='/dev/NULL')

    driver.implicitly_wait(15)
    try:
        driver.get(url=url)
        time.sleep(15)
        element = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/div/div/div/div/div/div[2]/div[2]')
        parsed_text = element.text

        with open('tmp.txt', 'w', encoding='utf-8') as output:
            output.write(parsed_text)

        with open('tmp.txt', 'r', encoding='utf-8') as file:
            lst1 = file.readlines()

        result = []
        for q in range(len(lst1)):
            rem = False
            for word in lst1[q].split():
                if word.strip() in exclude_list:
                    rem = True
            if not rem:
                if '₽' in lst1[q] and q > 1:
                    result.append('\n')
                result.append(lst1[q])

        with open(result_file, 'w', encoding='utf-8') as file:
            file.writelines(result)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def start_parse():
    current_time = str(datetime.datetime.now().time()).split('.')[0].split(':')
    current_time = current_time[0] + '.' + current_time[1]
    for i in range(1, 6):
        date = get_date_for_url(i)
        filename = f'{str(datetime.datetime.today()).split()[0]}_{current_time}_for_{date[:2]}.{date[2:]}.txt'
        try:
            parse_to_files(f'https://www.aviasales.ru/search/{from_city}{date}{to_city}1?request_source=expired_search', filename)
        except:
            pass
        time.sleep(1)
    # dictionary = form_dictionary()
    # show_ticket_dict(dictionary)
    # generate_graph_from_dict(dictionary)


def main():
    #start_parse()
    show_ticket_dict(form_dictionary())
    generate_graph_from_dict(form_dictionary())

    # schedule.every().day.at('00:34').do(start_parse)
    # schedule.every().day.at('00:37').do(start_parse)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == "__main__":
    main()



