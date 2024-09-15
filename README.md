# ToDoList

## build && configure 

### 1. Установка зависимостей
pip install -r requirements.txt  

### 2. Файлы конфигурации
#### Создайте файл .env-non-dev в папке main_service и задайте в нём параметры в формате:  
DB_HOST=text
DB_PORT=text
DB_USER=text
DB_PASS=text
DB_NAME=text

ALGORITHM=text - алгоритм для хэширования jwt токенов
TG_HASH_ALGORITHM=text - алгоритм для хэширования telegram id

REDIS_HOST=text
REDIS_PORT=text

SMTP_HOST=text - сервер почты (smtp.yandex.ru или smtp.gmail.com)
SMTP_PORT=text 
SMTP_USER=text
SMTP_PASS=text

#### Создайте файл .env-non-dev в папке comments_service и задайте в нём параметры в формате(база дынных отличается от базы в main_service):  
DB_HOST=text
DB_PORT=text
DB_USER=text
DB_PASS=text
DB_NAME=text

REDIS_HOST=text
REDIS_PORT=text

#### Создайте файл .env в папке bot и задайте в нём параметры в формате:  
BOT_TOKEN=text - токен бота(получаем при создании бота в BotFather)

TG_HASH_ALGORITHM=text - алгоритм для хэширования telegram id (тот же, что и в main_service)


### 3. Секретные ключи
#### Сгенерируйте секретный ключ командой:
openssl genrsa -out secret_key.pem 2048

#### Создайте файл secret_key.pem в папках bot и main_service с сгенерированным ключём


### 4. Запуск приложения
Запустите redis

#### Введите команду для запуска сервиса комментариев из папки comments_service:
uvicorn app.main:app --reload --port 8001

#### Введите команду для запуска основного сервиса из папки main_service:
uvicorn app.main:app --reload --port 8000

#### Введите команду для запуска бота из папки bot:
python -m app.main

#### Запустите celery из папки main_service:
celery -A app.celery_tasks.main_celery:celery beat --loglevel=INFO
celery -A app.celery_tasks.main_celery:celery worker --loglevel=info  (При запуске на windows добавить -P solo)
