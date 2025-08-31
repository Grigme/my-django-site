# My Django Site

Django-проект для разработки веб-приложения.

Веб сервис, который позволяет:

В режиме admin:
- [x] Создавать/изменять страницы.
- [x] Привязывать контент к страницам в любом количестве.
   - [x] url ссылки на видео и субтитры к видео.
   - [x] Аудио в виде текста произвольной длины.
В режиме пользователя:
- [x] Отображает список всех страниц с пагинацией.
- [x] Считает количество просмотров у каждого контента на странице в асинхронном режиме.


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
В другом терминале необходимо запустить кластер Django_q для обработки асинхронных задач
```bash
python manage.py qcluster
```
Перейдите по адресу http://127.0.0.1:8000/
## Запуск тестов
```bash
python manage.py test content.tests
```