# Moberries Pizza backend service

This is a test challenge for moberries interviewing process

## Getting Started

#### Built With:

* Django 3.0
* Django Rest Framework 3.10.3
* gunicorn
* Nginx
* Docker
* python 3.7
* PostgreSql 12.0

#### How to run:

* download and install docker (https://www.docker.com/products/docker-desktop)

* Pull project from github
`git clone https://github.com/eugeny-m/moberries_pizza.git`
* Go to project root
`cd moberries_pizza`
* build image `docker-compose build`
* run docker services `docker-compose up -d`

##### First Run

* create db `docker exec moberries_pizza_db_1 createdb moberries_pizza -U postgres --encoding=UTF8`
* run migrations `docker exec moberries_pizza_moberries_pizza_1 python manage.py migrate`
* run collectstatic `docker exec moberries_pizza_moberries_pizza_1 python manage.py collectstatic`

#### Endpoints

* localhost/api/v0.1/pizza (Create/change/delete/get pizza)
* localhost/api/v0.1/pizza-price (Create/change/delete/get pizza variants (size,price))
* localhost/api/v0.1/order (Create/change/delete/get order)
* localhost/api/v0.1/ordered-pizza (Create/change/delete/get order position)

#### Run tests
* create python environment
* `pip install -r requirements.txt`
* `python manage.py test`
