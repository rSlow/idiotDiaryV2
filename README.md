# Collection of Python Telegram [bots](https://t.me/idiotDiaryV2Bot) from [@rs1ow](https://t.me/rs1ow )

## Based on:
---

1. [python 3.11](https://www.python.org/downloads/release/python-3110)
2. [aiogram](https://aiogram.dev), `version: 3.1.1` - async Telegram bot app for Python
3. [aiogram-dialog](https://github.com/Tishka17/aiogram_dialog), `version: 2.2.0a3` - framework for developing
   interactive telegram messages
4. [SQLAlchemy](https://www.sqlalchemy.org), `version: 2.0` - ORM for Postgres database
5. [apscheduler](https://apscheduler.readthedocs.io/en/3.x/), `version: 3.10.4` - for scheduled tasks in birthdays app
6. [alembic](https://alembic.sqlalchemy.org/en/latest), `version: 1.12.0` - applying migrations to SQLAlchemy
7. [redis](https://redis.io/docs/connect/clients/python), `version: latest` - for using RedisStorage in aiogram
8. [aiohttp](https://docs.aiohttp.org/en/stable), `version: 4.0` - web server for webhook, as well as for HTTP requests
9. [nginx](https://hub.docker.com/_/nginx), `version: latest` - web server for aiohttp, + SSL
10. [selenium](https://hub.docker.com/r/selenium/standalone-chrome), `version: standalone-chrome`, as a docker
    container - for parsing sites
11. [eyed3](https://eyed3.readthedocs.io/en/latest), `version: 0.9.7` - editing MP3 tags
12. [yt-dlp](https://github.com/yt-dlp/yt-dlp), `version: 2023.10.13` - download videos from YouTube
13. [ffmpeg](https://www.ffmpeg.org), `version: latest (apt)` - downloader for yt-dlp
14. [Jinja2](https://jinja.palletsprojects.com), `version: 3.1.2` - generating template messages

## Bot Applications:
---

### 1. not working place 😶‍🌫️

- archiving photos (telegram photos and files) to a zip archive
- declensions of full name (in Russian) in all cases of the Russian language
- downloading a telegram video message (yes, I know that this function is in the official application, but I don't care
  😂)
- converting a voice message to a regular audio file
- checking the INN according to passport data (using selenium and parsing `https://service.nalog.ru/inn.do`)

### 2. free shawarma 🌯 - imitation of screenshots about transfers to various banks.

###### ONLY FOR TESTING!

### 3. music app 🎧

- async downloading music from YouTube, including downloading part of the video (based
  on [yt-dlp](https://github.com/yt-dlp/yt-dlp))
- MP3 tag editor (based on [eyeD3](https://eyed3.readthedocs.io/en/latest))

### 3. birthdays app 🎂

- notification of upcoming birthdays at a set time
- correction of time zones for correct notification
- ability to add multiple timestamps for notifications

### 4. Application for admins

- log files

## ENVIRONMENTS

---

#### The `.env` file is required to run in the root of the project.

### Required variables .env file:

| Env variable        | Mean                                                                                        |
|:--------------------|:--------------------------------------------------------------------------------------------|
| `BOT_TOKEN`         | telegram bot token                                                                          |
| `OWNER_ID`          | telegram account ID, for filtering admins                                                   |
| `BIRTHDAYS_ALLOWED` | telegram IDs of users who are allowed to use the birthdays app                              |
| `MORPH_URL`         | HTTP-endpoint for the FULL NAME declension service                                          |
| `BASE_WEBHOOK_URL`  | http address of the server (domain). Required for telegram webhook                          |
| `WEBHOOK_PATH`      | relative path for telegram webhook                                                          |
| `WEB_SERVER_PORT`   | internal aiohttp port                                                                       |
| `CERTS_DIR`         | path for SSL certificates. Generating certificates using [certbot](https://certbot.eff.org) |
| `POSTGRES_USER`     | the name of the PostgreSQL user                                                             |
| `POSTGRES_PASSWORD` | password for accessing PostgreSQL                                                           |
| `POSTGRES_DB`       | name of the PostgreSQL database                                                             |
| `POSTGRES_PORT`     | external port of PostgreSQL                                                                 |
| `DATABASE_URL`      | PostgreSQL URL for SQLAlchemy                                                               |
| `REDIS_PASS`        | password for redis storage                                                                  |
| `REDIS_URL`         | URL for RedisStorage in format `redis://:<password>@<host>/0`                               |
| `SELENIUM_PORT`     | external port of the selenium container                                                     |
| `SELENIUM_URL`      | the full URL of the selenium container, in the format `http://<selenium_address>/wd/hub`    |

### Optional variables .env file:

| Env variable        | Mean                                                                                |
|:--------------------|:------------------------------------------------------------------------------------|
| `DEBUG`             | debug mode                                                                          |
| `TIMEZONE`          | pytz timezone, required to send notifications using scheduler                       |
| `WEBHOOK_SECRET`    | secret token for checking the telegram validity of a webhook request                |
| `BASE_WEBHOOK_PORT` | port for telegram webhook. By default, `443`, but it is possible to use `8443` port |
| `LOGURU_FILE`       | the file where the logger 'loguru' will save logs                                   |

## DEPLOY

---

### Launch (2 options):

```bash
docker compose up -d
```

or

```bash
chmod +x ./start.sh && ./start.sh 
```

---

### Stop (2 options):

```bash
docker compose down
```

or

```bash
chmod +x ./stop.sh && ./stop.sh
```

---

### There is an update system (stop, update from github, launch) with the command

```bash
chmod +x ./update.sh && ./update.sh
```

## HTTP ENDPOINTS:

---

### 1. `/birthdays` [method - `PUT`]

### _All requests require a `user_id` request header equal to the telegram user id_

##### updating birthday rows

- **required**: request body [list of objects]

  ##### expected object fields:

    - **uuid**: _str_ `[unique UUID as SQL primary key]`
    - **fio**: _str_ `[Full name in the format Surname, First name, Patronymic]`
    - **rank**: _str_ | None `[Rank, may be missing]`
    - **post**: _str_ `[Post]`
    - **date**: _date_ `[Date in DD.MM.YYYY format]`

      ```json
      [
        {
          "uuid": "8db2a296-76f3-4d34-9f71-fa7cf213e4d3",
          "fio": "Иванов Роман Петрович",
          "rank": "лейтенант",
          "post": "Инспектор",
          "date": "12.01.1981"
        }
      ]
      ```

- **response**:

| Status | Explaining       |
|:-------|:-----------------| 
| `200`  | OK               |
| `422`  | validation error |

### 2. `/birthdays` [method - `DELETE`]

##### deleting all records (clearing)

- **response**:

| Status | Explaining |
|:-------|:-----------| 
| `200`  | OK         |

### 3. `/birthdays/{uuid}` [method - `DELETE`]

##### deleting a specific row with the uuid identifier

- **required**: path argument

  ##### expected path arguments:

    - **uuid**: _str_ `[unique UUID as SQL primary key]`

        ```http request
        [DELETE] /birthdays/8db2a296-76f3-4d34-9f71-fa7cf213e4d3
        ```

- **response**:

| Status | Explaining                       |
|:-------|:---------------------------------| 
| `200`  | OK                               |
| `404`  | row with this uuid was not found |
| `422`  | in case of validation error      |

## Python features:

---

- to run synchronous functions as asynchronous, set the decorator `@set_async`

    ```python
    @set_async
    def do_something():
        ...
    
    
    # or use as additional function
    
    await set_async(do_something)()
    ```

- to set the timer for the execution of an asynchronous function, the
  decorator `@coro_timer(seconds:int, exc:Exception)` is used, as a parameter takes time in seconds. After the time
  has elapsed, a custom exception can optionally be raised.

    ```python
    @coro_timer(10, exc=TimeoutError)
    async def do_something():
        ...
    ```

## Aiogram-dialog

---

### 1. WindowFactory

#### allows you to generate a dialog consisting of several (unlimited number of) windows according to a template

the number of windows is generated based on the transferred object `FormStatesGroup`, from which all `FormState` are
taken in order
it is possible to move back and forth through the data entry form

to create a dialog, you need to call the `.create_dialog()` method on the `WindowFactory()` object

```python
WindowFactory(
    states_group=some_states_group,
    on_finish=some_function_on_finish_form,
    template=WindowTemplate(...)
).create_dialog()
```

### 2. FormState

a modified State, to which the following has been added:

- additional buttons in the keyboard
- displaying the current state value
- binding an additional data getter
- and all the other functions inherent in the standard `TextInput` from aiogram-dialog... 
- (in future maybe i will add `MessageInput` support)

#### it is important to add `FormState` exclusively to `FormStatesGroup` class!

## NGINX

---

- #### nginx need SSL certificates for webhook aiogram. Env `CERTS_DIR` will be folder `/certs`, generated by certbot.

  f.e. un `.env` file:

    ```dotenv
    CERTS_DIR=~/certbot_certs/certs
    ```
- #### for nginx.conf needed to set domain, which will be used in setting path for ssl_certificate and ssl_certificate_key.
    ```dotenv
    DOMAIN=example.com
    ```
