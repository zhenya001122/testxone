"TESTXONE"
====

"API для хранения ссылок пользователя"
====

"При добавлении ссылки пользователь передает только url. Остальные данные сервис получает сам."

Author: Evgeny Shutko <sluckltu@gmail.com>

Requirements:

    Python 3.12, Django 5.1.3 и т.д.

## Установка:
1.  **Клонируйте репозиторий:**
    
    git clone [git@github.com:zhenya001122/testxone.git]

    cd [testxone]

2.  **Создайте виртуальное окружение:**
    
    python3 -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    venv\Scripts\activate  # Для Windows

3.  **Установите зависимости:**

    pip install -r requirements.txt

4.  **Настройте базу данных (если необходимо)**
5.  **Выполните миграции базы данных:**
    
    python manage.py migrate

6.  **Запустите сервер разработки:**

    python manage.py runserver
