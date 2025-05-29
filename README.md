# Проект: Yamdb API - Групповая работа

## Описание.

Проект **YaMDb** собирает отзывы **пользователей** на **произведения**. Сами **произведения** в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку.\
Произведения делятся на **категории**, такие как «Книги», «Фильмы», «Музыка». Например, в **категории** «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в **категории** «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список **категорий** может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).\
**Произведению** может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).\
Добавлять **произведения**, **категории** и **жанры** может только **Администратор**.\
Благодарные или возмущённые **пользователи** оставляют к **произведениям** текстовые **отзывы** и ставят произведению **оценку** в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка **произведения** — рейтинг (целое число). На одно **произведение** **пользователь** может оставить только один **отзыв**.\
**Пользователи** могут оставлять **комментарии** к **отзывам**.\
Добавлять **отзывы**, **комментарии** и ставить **оценки** могут только **аутентифицированные пользователи**.


## Технологии.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

## Установка проекта Ubuntu, Windows

Клонировать репозиторий:
```
git clone git@github.com:Dumskii-Artem/api_yamdb.git
```

Перейти в папку с проектом:
```
cd api_yamdb/
```
Cоздать виртуальное окружение:
```
Ubuntu: python3 -m venv env
Windows: py -3.9 -m venv env
```
Активировать виртуальное окружение:
```
Ubuntu: source env/bin/activate
Windows: source ./env/Scripts/activate
    или ./env/Scripts/activate
```
Вот так написать:
```
Ubuntu: python3 -m pip install --upgrade pip
Windows: python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Зайти в папку:
```
cd api_yamdb/
```
Выполнить миграции:
```
Ubuntu: python3 manage.py makemigrations
        python3 manage.py migrate
Windows: python manage.py makemigrations
         python manage.py migrate
```
Запустить скрипт для создания пользователей,
нужно для прохождения тестов

в среде Windows выполняется в GitBash
предварительно нужно создать виртуальное окружение в GitBash
```
bash ../postman_collection/set_up_data.sh 
```
Запустить проект:
```
Ubuntu: python3 manage.py runserver
Windows: python manage.py runserver
```


## Документация:

После запуска проекта, документация доступна по [ссылке](http://127.0.0.1:8000/redoc/)


## Импорт данных:

###  Импорт с путем по умолчанию:

```
...
```

## Тестирование: 

```
pytest
```

### Коллекция запросов для Postman:
В директории **postman_collection** сохранена коллекция 
запросов для отладки и проверки работы текущей версии API для проекта **YaMDB**.\
Инструкция по работе с коллекцией находится в файле **/postman_collection/README.md**.

### Примеры запросов


## Над проектом работают:

[Артём Думский](https://github.com/Dumskii-Artem) — Team Lead
* система регистрации и аутентификации
* права доступа
* работа с токеном
* система подтверждения через e-mail

[Виталий Мигаев](https://github.com/VitalyMigaev/)
* модели, view и эндпойнты для
    * произведений
    * категорий
    * жанров
* импорт данных из csv файлов.

[Дмитрий Василькин](https://github.com/Dmitriy-Vasilkin/)
* модели, view и эндпойнты для
    * отзывов
    * комментариев
    * рейтинга произведений



