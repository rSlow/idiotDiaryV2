import time

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter, RabbitExchange

from idiotDiary.bot.models.inn import INNSchema
from idiotDiary.mq.utils.selenuim import find_by_css, find_by_id

router = RabbitRouter()
selenium_exchange = RabbitExchange("selenium")


@router.subscriber("inn", selenium_exchange)
@inject
async def send_alert(inn_schema: INNSchema, webdriver: FromDishka[Remote]):
    # short function names
    wait = webdriver.implicitly_wait
    sleep = time.sleep

    try:
        webdriver.get("https://service.nalog.ru/inn.do")
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
            # `find_by_id(key).send_keys(value)`
            # pass some chars, idk why, i set some sleeping for stability
            _input = find_by_id(key)
            for c in value:
                _input.send_keys(c)
                sleep(0.03)
            sleep(0.1)

        find_by_id("btn_send").click()
        wait(3)

        inn_block = find_by_id("resultInn")
        if inn_block and (inn := inn_block.text):
            return inn

    finally:
        webdriver.close()

    ...
