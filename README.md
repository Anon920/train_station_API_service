# Train Station API Service

API service for managing train journeys.

## Installing using GitHub:

Install PostgreSQL and create db

```shell
git clone https://github.com/Anon920/train_station_API_service.git
cd train_station_API_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set DJANGO_DEBUG=<True/False>
set DJANGO_SECRET_KEY=<your secret key>
set POSTGRES_DB=<your db name>
set POSTGRES_HOST=<your db hostname>
set POSTGRES_PORT=<your db port>
set POSTGRES_USER=<your db username>
set POSTGRES_PASSWORD=<your db user password>
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Run with docker:

Docker should be installed

```shell
docker-compose build
docker-compose up
```

## Getting access:

- create user via /api/v1/user/register/
- get access token via /api/v1/user/token/

## Documentation:

- Documentation available via /api/v1/doc/swagger/

