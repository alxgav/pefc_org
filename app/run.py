import os
import re
import pandas as pd
from time import sleep
from config import browser

from loguru import logger

from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select


path = os.path.dirname(os.path.realpath(__file__)) 
logger.add(f'{path}/error.log', format='{time} {level} {message}', level='DEBUG', serialize=False)



browser = browser()


def init_page() -> None:
    browser.get('https://www.pefc.org/find-certified')
    sleep(5)
    cookies_click = browser.find_element(By.XPATH, '//*[@id="consent-allow"]')
    ActionChains(browser).click(cookies_click).perform()
    logger.info('cookies click')
    sleep(15)
    select = 'cbResultSetRecordPerPageControl'
    select_element = browser.find_element(By.CLASS_NAME, select)
    select_object = Select(select_element)
    select_object.select_by_value('250')
    logger.info('select pages by 250 position')
    sleep(15)
    


def getData() -> list[dict]:
    data = []
    try:
        init_page()
        total_pages = ''.join(re.findall('[0-9]+', browser.find_element(By.XPATH, '/html/body/div[2]/section[2]/div/div[2]/div/div/div/div/article/div[2]/div/div/article/form/div/nav/div[1]/ul[1]/li[3]/span').text))
        logger.info(total_pages)
        rows = len(browser.find_elements(By.CLASS_NAME, 'cbResultSetDataRow'))

        logger.info(rows)

        for page in range(1, int(total_pages)+1):
            logger.info(page)
            if page >=2:
                page_input = browser.find_element(By.CLASS_NAME, 'cbResultSetJumpToTextField')
                page_input.clear()
                page_input.send_keys(page)
                page_input.send_keys(Keys.ENTER)
                sleep(10)
            
            for row in range(1, rows+1):
                Entity =  browser.find_element(By.XPATH, f'/html/body/div[2]/section[2]/div/div[2]/div/div/div/div/article/div[2]/div/div/article/form/div/div/div/table/tbody/tr[{row}]/td[3]').text
                Certificate = browser.find_element(By.XPATH, f'/html/body/div[2]/section[2]/div/div[2]/div/div/div/div/article/div[2]/div/div/article/form/div/div/div/table/tbody/tr[{row}]/td[4]').text
                Licence = browser.find_element(By.XPATH, f'/html/body/div[2]/section[2]/div/div[2]/div/div/div/div/article/div[2]/div/div/article/form/div/div/div/table/tbody/tr[{row}]/td[5]').text
                data.append({
                    'Entity': Entity,
                    'Certificate': Certificate,
                    'Licence': Licence
                })
            # if page == 3:
            #     break
        return data

    except Exception as ex:
        logger.error(ex)
    finally:
        # pass
        browser.close()
        browser.quit()

def make_excel(data, filename='out/data.xlsx', sheet_name='sheet') -> None:

    df = pd.json_normalize(data)
    writer = pd.ExcelWriter(filename)

    df.to_excel(writer, sheet_name=sheet_name, index=False, na_rep='NaN')

    workbook = writer.book

    worksheet = writer.sheets[sheet_name]
    worksheet.set_default_row(hide_unused_rows=True)
    center_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
    header_format = workbook.add_format({'bold': True,
                                         'fg_color': '#D4D3D3',
                                         'border': 1, 'text_wrap': True,
                                         'align': 'center', 'valign': 'vcenter'})
    for col_num, value in enumerate(df.columns.values):
        worksheet.set_row(0, 50)
        writer.sheets[sheet_name].set_column(0, col_num, len(value)+60, center_format)
        worksheet.write(0, col_num, value, header_format)
    worksheet.set_default_row(50)

    writer.save()





@logger.catch
def main():
    make_excel(getData())
   

if __name__ in "__main__":
    main()
