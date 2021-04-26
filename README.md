```
 ____  _                  ____           _   
/ ___|| |__   ___  _ __  / ___|__ _ _ __| |_ 
\___ \| '_ \ / _ \| '_ \| |   / _` | '__| __|
 ___) | | | | (_) | |_) | |__| (_| | |  | |_ 
|____/|_| |_|\___/| .__/ \____\__,_|_|   \__|
                  |_|                        
                                                                                             
```
---

<h1 align="center">Django Implementing ShopCart</h1>

<p align="center">
<a href="https://github.com/psf/black">
<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

### Project Description
- ShopCart implement the shop-cart demo with django, including of add orders, delete orders, and get hottest products.

### Enviroment:
- Python: 3.8
- Fronend: Bootstrap
- Backend: Django Rest Framework
- Database: SQLite
- Cronjob: Celery

### Visit Home page
- http://127.0.0.1:8000/index/

### Deploy Applications:
```
$ cd docker
$ sudo docker-compose up --build -d
```

### Visit interactive back-platform to test api
```bash
python manage.py runserver
```
- visit: http://localhost:8000/


### Cronjob (Celery beat)
```bash
celery beat -A Urmart.tasks -l info
celery worker -A Urmart.tasks -l info
```
