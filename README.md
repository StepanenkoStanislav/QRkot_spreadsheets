# Приложение для Благотворительного фонда поддержки котиков QRKot

## Описание проекта

Фонд собирает пожертвования на различные целевые проекты: 
на медицинское обслуживание нуждающихся хвостатых, на обустройство 
кошачьей колонии в подвале, на корм оставшимся без попечения 
кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

### Проекты

В Фонде QRKot может быть открыто несколько целевых проектов. 
У каждого проекта есть название, описание и сумма, которую планируется собрать. 
После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все 
пожертвования идут в проект, открытый раньше других; когда этот проект 
набирает необходимую сумму и закрывается — пожертвования начинают поступать 
в следующий проект.

### Пожертвования

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. 
Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое 
полученное пожертвование автоматически добавляется в первый открытый проект, 
который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или 
же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего
проекта. При создании нового проекта все неинвестированные пожертвования 
автоматически вкладываются в новый проект.

### Пользователи
Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и 
уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и 
просматривать список своих пожертвований.

### Отчеты
В приложении QRKot для администраторов есть возможность формирования
отчета в Гугл-таблице. В таблице будут закрытые проекты, отсортированные
по скорости сбора средств - от тех, что закрылись быстрее всего, до
тех, что долго собирали нужную сумму.


## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:StepanenkoStanislav/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

В директории _QRkot_spreadsheets_ необходимо создать файл _.env_
(Пример находится в QRkot_spreadsheets/example.env), где необходимо указать:
```
SECRET=ThisIsSecret - Секретный ключ
FIRST_SUPERUSER_EMAIL=superuser@mail.com - Email первого суперюзера
FIRST_SUPERUSER_PASSWORD=Password - Пароль первого суперюзера
DATABASE_URL=sqlite+aiosqlite:///./cat_charity_fund.db - Используемая БД

EMAIL=youremail@gmail.com  # Ваш gmail
TYPE=service_account
PROJECT_ID=your_project_id  # ID проекта
PRIVATE_KEY_ID=your_private_key_id  # ID приватного ключа
PRIVATE_KEY=your_private_key  # Приватный ключ
CLIENT_EMAIL=your_client_email  # Email клиента
CLIENT_ID=your_client_id  # ID клиента
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=your_cert_url
```

### Запуск

Находясь в директории _QRkot_spreadsheets_ введите в терминале команду 
для настройки БД
```commandline
alembic upgrade head
```
Затем введите команду для запуска проекта
```commandline
uvicorn app.main:app
```
По умолчанию проект будет доступен по адресу http://127.0.0.1:8000

Описание ендпоинтов API по умолчанию будет доступно по адресу 
http://127.0.0.1:8000/docs

### Примеры запросов

- GET запрос к /charity_project/ - получение всех благотворительных проектов

Ответ
```
[
  {
    "name": "charity project name",
    "description": "charity project description",
    "full_amount": 10000,
    "id": 1,
    "invested_amount": 10000,
    "fully_invested": true,
    "create_date": "2023-10-10T20:26:58.742261",
    "close_date": "2023-10-10T20:27:49.067720"
  }
]
```

## Технологии

В проекте используются следующие технологии:

- Python 3.7
- FastAPI 0.78.0
- Alembic 1.7.7
- SQLAlchemy 1.4.36
- Pydantic 1.9.1
- Uvicorn 0.17.6
- Aiogoogle 4.2.0

## Автор

[Степаненко Станислав](https://t.me/tme_zoom)

[![Telegram Badge](https://img.shields.io/badge/StepanenkoStanislav-blue?logo=telegram&logoColor=white)](https://t.me/tme_zoom) [![Gmail Badge](https://img.shields.io/badge/-Gmail-red?style=flat&logo=Gmail&logoColor=white)](mailto:stepanenko.s.a.dev@gmail.com)
