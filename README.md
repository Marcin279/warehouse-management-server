# warehouse-management-server

Server for Web application to support warehouse management
Required Tools:
- Python 3.10
- PostgreSQL database
- Docker
- pgAdmin4/DataGrip

Database settings is set in settings.py file

## How to run App
### Libraries
- asgiref==3.5.2
- Django==4.1.3
- django-environ==0.9.0
- djangorestframework==3.14.0
- psycopg2-binary==2.9.5
- pytz==2022.6
- sqlparse==0.4.3
- tzdata==2022.6
- pip==22.3
- wheel~=0.37.1
- setuptools==65.5.0

## Install libraries
Use Python 3.10.0, 3.11 cause error with psycopg2 library

`pip install requirements.txt`

## Prepare virtual environment
### Create virtual environment
`python -m venv env_name`

### Activate virualenv
`.\env_name\Scripts\activate`

## Run App
Server is set to localhost:8080

`python manage.py runserver` </br>

## Develop
Making migration

`python manage.py makemigrations`

### Migrate data

`python manage.py migrate`

### Run app

`python manage.py runserver`

# Docker Version
1. Clone Repo
2. Create Container & Build dependencies `docker-compose up`
3. To enter container`docker exec -it {container_id} bash`
4. To rebuild container `docker-compose build {name}`
