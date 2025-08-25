# My Django Site

Django-проект для разработки веб-приложения.

## Предварительные требования

- Python 3.8 или выше
- Git
- Виртуальное окружение (virtualenv)

## Запуск проекта

Для Windows
```bash
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Перейдите по адресу http://127.0.0.1:8000/