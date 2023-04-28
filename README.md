# Simple-API
* http://localhost:8080/auth - авторизация через Githaub
* http://localhost:8080/product - получить все товары
* http://localhost:8080/product/?price= - отфильтровать результаты по цене
* http://localhost:8080/product/?search= - поиск
* http://localhost:8080/product/?ordering= - сортировка по цене или имени
* http://localhost:8080/product/{product_id} - получение изменение и удаление конкретного товара
* http://localhost:8080/product_relation/{product_id}?rate= - изменение рейтинга товара
* http://localhost:8080/product_relation/{product_id}?in_bookmarks={bool} - добавление в закладки
* http://localhost:8080/product_relation/{product_id}?like={bool} - лайк товара


# stack
* python 3.11
* Django 4.2
* django rest framework 3.14
* Postgresql 15
* Docker, docker-compose

# starting

Изменить данные в файле .env.dev или оставить их тестовыми

Запустить командой
* docker-compose up -d --build

Создать админа командой
* docker-compose exec web python manage.py createsuperuser

