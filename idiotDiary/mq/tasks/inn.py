import time
from functools import partial

from dishka import FromDishka
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from idiotDiary.bot.schemas.inn import INNSchema
from idiotDiary.mq.broker import broker
from idiotDiary.mq.di.inject import inject, sync_inject
from idiotDiary.mq.utils.types.selenium import PartialFind


@broker.task
@sync_inject
def get_inn(data: dict, driver: FromDishka[WebDriver]):
    inn_schema = INNSchema.model_validate(data)
    # short function names
    wait = driver.implicitly_wait
    sleep = time.sleep
    find_by_id: PartialFind = partial(driver.find_element, By.ID)
    find_by_css: PartialFind = partial(driver.find_element, By.CSS_SELECTOR)

    driver.get("https://service.nalog.ru/inn.do")
    wait(10)
    find_by_css(".checkbox-item > a.checkbox").click()
    find_by_id("btnContinue").click()
    wait(10)

    fam, nam, otch = inn_schema.fio.split()
    values = {
        "fam": fam,
        "nam": nam,
        "otch": otch,
        "bdate": inn_schema.birthday,
        "docno": inn_schema.passport,
        "docdt": inn_schema.date_passport or "",
    }
    for key, value in values.items():
        # find_by_id(key).send_keys(value)
        # pass some chars, idk why, i set some sleeping for stability
        _input = find_by_id(key)
        for c in value:
            _input.send_keys(c)
            wait(0.02)
        wait(0.02)

    find_by_id("btn_send").click()
    sleep(3)

    inn_block = find_by_id("resultInn")
    if inn_block and (inn := inn_block.text):
        return inn
