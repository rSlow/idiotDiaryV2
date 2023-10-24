import time
from typing import Callable

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..filters.inn_filter import INNSchema


def get_inn_selenium(data: INNSchema):
    options = Options()
    args = ['--headless', 'window-size=1920x1080', "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]
    [options.add_argument(arg) for arg in args]

    driver = webdriver.Chrome(options=options)

    # short function names
    find_by_id: Callable[[str], WebElement] = lambda id_value: driver.find_element(By.ID, id_value)
    find_by_css: Callable[[str], WebElement] = lambda css_value: driver.find_element(By.CSS_SELECTOR, css_value)
    wait = driver.implicitly_wait
    sleep = time.sleep

    try:
        driver.get("https://service.nalog.ru/inn.do")
        wait(10)
        find_by_css(".checkbox-item > a.checkbox").click()
        find_by_id("btnContinue").click()
        wait(10)

        fam, nam, otch = data.fio.split()
        values = {
            "fam": fam,
            "nam": nam,
            "otch": otch,
            "bdate": data.birthday,
            "docno": data.passport,
            "docdt": data.date_passport or "",
        }
        for key, value in values.items():
            # find_by_id(key).send_keys(value) # pass some chars, idk why, i set some sleeping for stability
            _input = find_by_id(key)
            for c in value:
                _input.send_keys(c)
                sleep(0.02)
            sleep(0.1)

        find_by_id("btn_send").click()
        sleep(3)

        inn_block = find_by_id("resultInn")
        return inn_block.text if inn_block is not None else None

    finally:
        driver.close()
        driver.quit()
