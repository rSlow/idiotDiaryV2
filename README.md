## Collection of Python Telegram [bots](https://t.me/idiotDiaryV2Bot) from [@rs1ow](https://t.me/rs1ow )

### Based on:

1. [python 3.11](https://www.python.org/downloads/release/python-3110)
2. [aiogram](https://aiogram.dev), version: 3.1.1 - async Telegram bot app for Python
3. [SQLAlchemy](https://www.sqlalchemy.org), version: 2.0 - ORM for Postgres database
4. [alembic](https://alembic.sqlalchemy.org/en/latest), version: 1.12.0 - applying migrations to SQLAlchemy
5. [redis](https://redis.io/docs/connect/clients/python), version: latest - for using RedisStorage in aiogram
6. [aiohttp](https://docs.aiohttp.org/en/stable), version: 4.0 - web server for webhook, as well as for HTTP requests
7. [nginx](https://hub.docker.com/_/nginx), version: latest - web server for aiohttp, + SSL
8. [selenium](https://hub.docker.com/r/selenium/standalone-chrome), version: standalone-chrome, as a docker container -
   for parsing sites
9. [eyed3](https://eyed3.readthedocs.io/en/latest), version: 0.9.7 - editing MP3 tags
10. [yt-dlp](https://github.com/yt-dlp/yt-dlp), version: 2023.10.13 - download videos from YouTube
11. [ffmpeg](https://www.ffmpeg.org), version: latest (apt) - downloader for yt-dlp
12. [Jinja2](https://jinja.palletsprojects.com), version: 3.1.2 - generating template messages

---

### Bot Applications:

#### 1. not working place 😶‍🌫️

- archiving photos (telegram photos and files) to a zip archive
- declensions of full name (in Russian) in all cases of the Russian language
- downloading a telegram video message (yes, I know that this function is in the official application, but I don't care
  😂)
- checking the INN according to passport data (using selenium and parsing https://service.nalog.ru/inn.do)
- checking birthdays (only for admins)
- auto-sending information about birthdays every day at 10 AM

#### 2. free shawarma 🌯 - imitation of screenshots about transfers to various banks.

###### ONLY FOR TESTING!

#### 3. music app 🎧

- async downloading music from YouTube, including downloading part of the video (based
  on [yt-dlp](https://github.com/yt-dlp/yt-dlp))
- MP3 tag editor (based on [eyeD3](https://eyed3.readthedocs.io/en/latest))

#### 4. Application for admins

- clearing birthdays
- log files

---

#### A .env file is required to run in the root of the project.

### Required variables .env file:

    --- AIOGRAM ENVS ---
    
      - BOT_TOKEN - telegram bot token
      - TIMEZONE - pytz timezone, required to send notifications using scheduler
      - OWNER_ID - Telegram account ID, for filtering admins and accessing individual menu items
      - MORPH_URL - HTTP-endpoint for the FULL NAME declension service
    
    --- HTTP ENVS ---
    
      - WEBHOOK_PATH - relative path for telegram webhook
      - BASE_WEBHOOK_URL - http address of the server (domain). Required for telegram webhook
      - BASE_WEBHOOK_PORT - port for telegram webhook. By default, 443, but it is possible to use 8443 ports
      - WEB_SERVER_PORT - internal aiohttp port
      - WEBHOOK_SECRET - secret token for checking the telegram validity of a webhook request
      - CERTS_DIR - path for SSL certificates. Generating certificates using [certbot](https://certbot.eff.org /)
    
    --- DATABASE ENVS ---
    
      - POSTGRES_USER - the name of the PostgreSQL user
      - POSTGRES_PASSWORD - password for accessing PostgreSQL
      - POSTGRES_DB - name of the PostgreSQL database
      - POSTGRES_PORT - external port of PostgreSQL
      - DATABASE_URL - PostgreSQL URL for SQLAlchemy
    
    --- OTHER ENVS ---
    
      - REDIS_PASS - password for redis storage
      - SELENIUM_PORT - external port of the selenium container
      - SELENIUM_URL - the full URL of the selenium container, in the format http://<selenium_address>/wd/hub

### Optional variables .env file:

    - aah

---

### Launch (2 options):

    1. docker compose up -d
    2. chmod +x ./start.sh && ./start.sh

### Stop (2 options):

    1. docker compose down
    2. chmod +x ./stop.sh && ./stop.sh

### There is an update system (stop, update from github, launch) with the command

    chmod +x ./update.sh && ./update.sh

---

### HTTP ENDPOINTS:

#### 1. /birthdays (method - `PUT`) - updating records.

The request body is expected - **list of objects**

##### expected object fields:

- **uuid**: _str_ `[unique UUID as SQL primary key]`
- **fio**: _str_ `[Full name in the format Surname, First name, Patronymic]`
- **rank**: _str_ | None `[Rank, may be missing]`
- **post**: _str_ `[Post]`
- **date**: _date_ `[Date in DD.MM.YYYY format]`

##### response:

    - 200 - OK
    - 422 - in case of validation error

#### 2. **/birthdays** (method - `DELETE`) - deleting all records (clearing)

##### response:

    - 200 - OK

#### 3. **/birthdays/{uuid}** (method - `DELETE`) - deleting a specific record with a uuid identifier.

Expected path arguments:

- **uuid**: _str_ `[unique UUID as SQL primary key]`

##### response:

    - 200 - OK
    - 404 - row with this uuid was not found
    - 422 - in case of validation error

---

### Features:

- to run synchronous functions as asynchronous, the decorator `@set_async` is used
- to set the timer for the execution of an asynchronous function, the decorator `@coro_timer('seconds:int')` is used, as
  a parameter takes time in seconds
- to create your own keyboards, `BaseKeyboardBuilder` is used, namely the classes inherited from it
  `BaseReplyKeyboardBuilder` and `BaseInlineKeyboardBuilder`
- in `BaseReplyKeyboardBuilder` it is possible to add buttons with the validator `BaseButtonValidator`, based on the
  builder will be
  make a decision about adding or not adding a button to the keyboard
- It is possible to use the modified aiogram storage `MemoryStorage` - `ModifiedMemoryStorage`
    - the point is that redis in **pooling** mode does not have time to save data to storage, which is why some of the
      data may get lost.
    - MemoryStorage does not have such a problem, but at the same time it is impossible to save even the FSM state in
      MemoryStorage.
    - ModifiedMemoryStorage allows you to store states in SQL, in a separate states table - and load them pre
      reboot the bot. However, the storage data will still be lost on reboot. However, such a way out is still
      better than the possible loss of data when saving to redis.
    - **BUT**: in the bot launch mode via webhook, this problem with redis is irrelevant.