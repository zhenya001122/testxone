# Используем официальный python-образ для начала
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем нужные файлы в контейнер
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем наше приложение в контейнер
COPY . .

# Указываем команду для выполнения нашего Django-приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]