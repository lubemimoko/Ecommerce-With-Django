from django.apps import AppConfig


class CrudappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecom'



'''

PROJECT
1. settings -> INSTALLED_APPS, DATABASES, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
2. rename project folder
3. rename project name in asgi.py(1), wsgi.py(1), settings.py(2), manage.py(1)
2. urls, path('', include("crudapi"))


APP
1. rename app folder
2. apps.py -> name='crudapp'
3. template -> folder contain our html files to match the app name
4. static -> folder contain our html files to match the app name


pipenv shell
pipenv install
'''