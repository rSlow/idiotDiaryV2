## Сборник Python Telegram ботов от [@rs1ow](https://t.me/rs1ow)

### За основу взяты:

1. [python 3.11](https://www.python.org/downloads/release/python-3110/)
2. [aiogram](https://aiogram.dev/), версия: 3.1 - обработчик для Telegram
3. [SQLAlchemy](https://www.sqlalchemy.org/), версия: 2.0 - ORM для Postgres базы данных
4. [redis](https://redis.io/docs/connect/clients/python/), версия: latest - для использования RedisStorage в aiogram
5. [aiohttp](https://docs.aiohttp.org/en/stable/), версия: 4.0 - веб-сервер для webhook, а также для HTTP-запросов
6. [selenium](https://hub.docker.com/r/selenium/standalone-chrome), версия: standalone-chrome, как docker-контейнер -
   для парсинга сайтов
7. [nginx](https://hub.docker.com/_/nginx), версия: latest - веб-сервер для aiohttp, + SSL

---

### Приложения бота:

#### 1. (не)рабочая площадка 😶‍🌫️

- архивация фото (telegram-фото и файлов) в zip-архив
- склонения ФИО (на русском языке) по всем падежам русского языка
- скачивание видеосообщения telegram (да, я знаю, что эта функция есть в официальном приложении, но мне плевать 😂)
- проверка ИНН по данным паспорта (с помощью selenium и парсинга https://service.nalog.ru/inn.do)
- проверка дней рождений (только для админов)
- автоотправка информации о днях рождения каждый день в 10 часов утра

#### 2. (бес)платная шаурма 🌯 - имитация скриншотов о переводах на различные банки.

###### ИСКЛЮЧИТЕЛЬНО ДЛЯ ТЕСТИРОВАНИЯ!

#### 3. музыка 🎧

- скачивание музыки с YouTube, в том числе скачивание части видео (на основе [yt-dlp](https://github.com/yt-dlp/yt-dlp))
- редактор тегов MP3 (на основе [eyeD3](https://eyed3.readthedocs.io/en/latest/))

#### 4. Приложение для админов

- очистка дней рождений
- файлы логов

---

#### Для запуска в корне проекта необходим .env файл.

### Обязательные переменные .env файла:

      --- AIOGRAM ENVS ---
      - **BOT_TOKEN** - токен telegram бота
      - **TIMEZONE** - pytz timezone, необходима для отправки уведомлений с помощью scheduler
      - **OWNER_ID** - Telegram account ID, для фильтрации админов и доступа к отдельным пунктам меню
      - **MORPH_URL** - HTTP-endpoint для сервиса по склонению ФИО
      
      --- HTTP ENVS ---
      - **WEBHOOK_PATH** - относительный путь для telegram webhook
      - **BASE_WEBHOOK_URL** - http-адрес сервера (домен). Необходим для telegram webhook
      - **BASE_WEBHOOK_PORT** - порт для telegram webhook. По умолчанию 443, но возможно использование и 8443 порта
      - **WEB_SERVER_PORT** - внутренний порт aiohttp
      - **WEBHOOK_SECRET** - секретный токен для проверки telegram валидности webhook-запроса
      - **CERTS_DIR** - путь для сертификатов SSL. Генерация сертификатов с помощью [certbot](https://certbot.eff.org/)

      --- DATABASE ENVS ---    
      - **POSTGRES_USER** - имя пользователя PostgresQL
      - **POSTGRES_PASSWORD** - пароль для доступа к PostgresQL
      - **POSTGRES_DB** - имя базы данных PostgresQL
      - **POSTGRES_PORT** - внешний порт PostgresQL
      - **DATABASE_URL** - URL PostgresQL для SQLAlchemy

      --- OTHER ENVS ---
      - **REDIS_PASS** - пароль для redis-хранилища
      - **SELENIUM_PORT** - внешний порт контейнера selenium
      - **SELENIUM_URL** - полный URL контейнера selenium, в формате http://<selenium_address>/wd/hub

### Необязательные переменные .env файла:

      - ааа

---

### Запуск (2 варианта):

      1. docker compose up -d
      2. chmod +x ./start.sh && ./start.sh

### Остановка (2 варианта):

      1. docker compose down
      2. chmod +x ./stop.sh && ./stop.sh

### Присутствует система обновления (остановка, обновление с github, запуск) командой

      chmod +x ./update.sh && ./update.sh

---

### HTTP ENDPOINTS:

#### 1. **/birthdays** (метод - PUT) - обновление записей.

Ожидается тело запроса - **список объектов**

##### ожидаемые поля объекта:

      - **uuid**: str [уникальный UUID, как первичный ключ SQL]
      - **fio**: str [ФИО в формате Фамилия, Имя, Отчество]
      - **rank**: str | None [Звание, может отсутствовать]
      - **post**: str [Должность]
      - **date**: date [Дата в формате DD.MM.YYYY]

##### ответ:

      - 200 - OK
      - 422 - при ошибке валидации

#### 2. **/birthdays** (метод - DELETE) - удаление всех записей (очистка)

##### ответ:

    - 200 - OK

#### 3. **/birthdays/{uuid}** (метод - DELETE) - удаление конкретной записи с uuid идентефикатором.

Ожидается аргумент path - **uuid**: str `[уникальный UUID, как первичный ключ SQL]`

##### ответ:

      - 200 - OK
      - 404 - запись к данным uuid не найдена
      - 422 - при ошибке валидации

---

