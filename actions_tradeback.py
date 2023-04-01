import time
from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from TradeBotEntities.settings_tradeback import SettingsTradebackForBuyTm
from TradeBotEntities.settings_tradeback import SettingsTradebackForBuySteam
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver


def authorization_on_tradeback(driver, login: str, password: str):
    try:
        url_comprasion = 'https://tradeback.io/ru/comparison'
        driver.get(url=url_comprasion)
        driver.maximize_window()
        element_login_steam = WebDriverWait(driver, 20).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "input[type=text].newlogindialog_TextInput_2eKVn")))
        element_password_steam = WebDriverWait(driver, 20).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "input[type=password].newlogindialog_TextInput_2eKVn")))
        element_login_steam.send_keys(login)
        element_password_steam.send_keys(password)
        element_get_in = WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, ".newlogindialog_SubmitButton_2QgFE")))
        element_get_in.click()
        try:
            steam_code = input("Введите код аутентификатора")
            steam_code_1_simbol = steam_code[0]
            steam_code_2_simbol = steam_code[1]
            steam_code_3_simbol = steam_code[2]
            steam_code_4_simbol = steam_code[3]
            steam_code_5_simbol = steam_code[4]

            element_input_1_simbol = driver.find_element(By.CSS_SELECTOR, '.newlogindialog_SegmentedCharacterInput_1kJ6q input:nth-child(1)')
            element_input_2_simbol = driver.find_element(By.CSS_SELECTOR,
                                                         '.newlogindialog_SegmentedCharacterInput_1kJ6q input:nth-child(2)')
            element_input_3_simbol = driver.find_element(By.CSS_SELECTOR,
                                                         '.newlogindialog_SegmentedCharacterInput_1kJ6q input:nth-child(3)')
            element_input_4_simbol = driver.find_element(By.CSS_SELECTOR,
                                                         '.newlogindialog_SegmentedCharacterInput_1kJ6q input:nth-child(4)')
            element_input_5_simbol = driver.find_element(By.CSS_SELECTOR,
                                                         '.newlogindialog_SegmentedCharacterInput_1kJ6q input:nth-child(5)')
            element_input_1_simbol.send_keys(steam_code_1_simbol)
            element_input_2_simbol.send_keys(steam_code_2_simbol)
            element_input_3_simbol.send_keys(steam_code_3_simbol)
            element_input_4_simbol.send_keys(steam_code_4_simbol)
            element_input_5_simbol.send_keys(steam_code_5_simbol + Keys.ENTER)

            try:
                element_last_get_in = WebDriverWait(driver, 5).until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, ".btn_green_white_innerfade")))
                element_last_get_in.click()
            except Exception as ex:
                print(f'Вроде зашел')
        except Exception as ex:
            print(f'{ex}, Не правильный код')
            driver.close()
            driver.quit()
    except Exception as ex:
        print(f'{ex}, Ошибка авторизации')
        driver.close()
        driver.quit()
    time.sleep(40)


def switch_to_tradeback(driver):
    driver.switch_to.window(driver.window_handles[0])


def get_course(driver):
    settings = WebDriverWait(driver, 60).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '#nav-menu .nav-page[href="/ru/settings"]')))
    settings.click()
    course_button = WebDriverWait(driver, 60).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '[for = "tab-courses"]')))
    course_button.click()
    course_window = WebDriverWait(driver, 60).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '#course_usdrub')))
    course = course_window.get_attribute("value")
    course = Decimal(course)
    return course


def settings_tradeback_for_buy_tm(driver, settings_tradeback_for_buy_on_tm: SettingsTradebackForBuyTm):
    load_page_wait = WebDriverWait(driver, 60).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "a.site-logo")))
    url_comprasion = 'https://tradeback.io/ru/comparison'
    driver.get(url=url_comprasion)
    # Game
    game_element = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, '.comparison-main-filters > div:nth-child(3)>div.title')))
    game_element.click()
    game_num = settings_tradeback_for_buy_on_tm.game
    game = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          f'.comparison-main-filters > div:nth-child(3) .menu-container li:nth-child({game_num})')))
    game.click()
    # Filter
    filter_items_element = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, '.comparison-main-filters > div:nth-child(4)>div.title')))
    filter_items_element.click()
    no_souvenir = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "label[for='filter-without-souvenir']")))
    no_souvenir.click()
    additional_filters_element = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, '.comparison-header .comparison-filters-btn')))
    additional_filters_element.click()
    steam_week_sales = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, '.comparison-sales-block:nth-child(1)>input')))
    steam_week_sales.clear()
    steam_week_sales.send_keys(settings_tradeback_for_buy_on_tm.steam_week_sales)
    close_additional_filters_element = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          '#filters-modal .iziModal-header-buttons>a:nth-child(1)')))
    close_additional_filters_element.click()
    # First Service
    first_service_element = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, '.comparison-service:nth-child(1) .dropdown-select')))
    first_service_element.click()
    first_service = settings_tradeback_for_buy_on_tm.first_service
    first_service = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          f".comparison-service:nth-child(1) ul.list>li[data-short-name = {first_service}]")))
    first_service.click()
    # Second Service
    second_service_element = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, '.comparison-service:nth-child(2) .dropdown-select')))
    second_service_element.click()
    second_service = settings_tradeback_for_buy_on_tm.second_service
    second_service = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          f".comparison-service:nth-child(2) ul.list>li[data-short-name = {second_service}]")))
    second_service.click()
    # First Service Price And Count
    # Price From
    first_service_price_from = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          ".center div.price-filters[data-column='first']>input:nth-child(2)")))
    first_service_price_from.clear()
    first_service_price_from.send_keys(settings_tradeback_for_buy_on_tm.first_service_price_from)
    # Count From
    first_service_count_from = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          ".center div.count-filters[data-column='first']>input:nth-child(2)")))
    first_service_count_from.clear()
    first_service_count_from.send_keys(settings_tradeback_for_buy_on_tm.first_service_count_from)

    # Sort
    first_sort = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          ".column-profit[data-column='first']")))
    first_sort.click()
    try:
        sort = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR,
                                              "div.column-profit[data-column='first']>i.fa-sort-amount-asc")))
        new_sort = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, ".column-profit[data-column='first']")))
        new_sort.click()
    except Exception as ex:
        pass

    # Procent First
    # Procent First From
    first_service_procent_from = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          ".profit-filters[data-column='first']>input:nth-child(2)")))
    first_service_procent_from.clear()
    first_service_procent_from.send_keys(settings_tradeback_for_buy_on_tm.first_service_procent_from)
    # Procent First Before
    first_service_procent_before = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          ".profit-filters[data-column='first']>input:nth-child(4)")))
    first_service_procent_before.clear()
    first_service_procent_before.send_keys(settings_tradeback_for_buy_on_tm.first_service_procent_before)

    refresh_table = WebDriverWait(driver, 20).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          "#table-refresh")))
    refresh_table.click()


def get_items_from_table(driver):
    first_elem_in_table = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, ".price-table tbody tr:nth-child(1)")))
    all_items = driver.page_source
    return all_items


def refresh_table(driver):
    refresh_table = WebDriverWait(driver, 3).until(ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          "#table-refresh")))
    refresh_table.click()
