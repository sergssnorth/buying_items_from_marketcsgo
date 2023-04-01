import time
from TradeBotEntities.settings_tradeback import SettingsTradebackForBuyTm
from TradeBotEntities.Enums import enum_games as games
from TradeBotEntities.Enums import services as services
from selenium import webdriver
from selenium_stealth import stealth
import actions_tradeback
import scraping_html
import asyncio
import actions_tm
#ooooqwe
# api_key = '8wHglF472LmGV5dR5T3NO9J23EIRAWG'

#Abany
api_key = '49o2PAU0PkYB0g5AQPgMd1u8bx270E8'

# Svarshik
# api_key = 'X7a9TVT8zxz36U0eT65uDl3YyMybqKj'

#danilbatka228
#api_key = 'C22JThLkawwJ0mO47V92lK4IeqPRT1Z'
# steam_login_for_tradeback = 'danilbatka'
# steam_password_for_tradeback = 'ROMANOVnba27012002'
steam_login_for_tradeback = 'ooooqwe'
steam_password_for_tradeback = 'skeletonking228'

#######################################################################################################################
# steam_week_sales = int(input("Введите кол-во продаж в неделю, (70) =>"))
# first_service_price_from = float(input("Введите от какой цены делать закуп, (0.5) =>"))
# procent = int(input("Введите процент, (15) =>"))
steam_week_sales = 70
first_service_price_from = 0.5
procent = 18
#######################################################################################################################
settings_tradeback_for_buy_on_tm = SettingsTradebackForBuyTm(game=games.Games.all.value,
                                                             steam_week_sales=steam_week_sales,
                                                             first_service=services.Services.tm_market.value,
                                                             second_service=services.Services.steam.value,
                                                             first_service_price_from=first_service_price_from,
                                                             first_service_count_from='1',
                                                             first_service_procent_from='3',
                                                             first_service_procent_before='250')
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
driver.set_window_size(1936, 1056)
print(driver.get_window_size())

actions_tradeback.authorization_on_tradeback(driver, steam_login_for_tradeback, steam_password_for_tradeback)
actions_tradeback.switch_to_tradeback(driver)
course_usdrub = actions_tradeback.get_course(driver)
actions_tradeback.settings_tradeback_for_buy_tm(driver, settings_tradeback_for_buy_on_tm)
print("Настройка завершена")
while True:
    try:
        start_time = time.time()
        all_items_html = actions_tradeback.get_items_from_table(driver)
        all_items = scraping_html.scraping_tradeback_comprassion(all_items_html)
        filtred_items = scraping_html.filter_out_items(all_items,course_usdrub, procent)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(actions_tm.buy_all_filterd_items(api_key, filtred_items))
        print("--- %s seconds ---" % (time.time() - start_time))
    except Exception as exception:
        print(f"Failed {exception}")

