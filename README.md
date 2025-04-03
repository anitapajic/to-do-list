# To-Do List

This is Django project `to_do_project`, with application `to_do_app` and PostgreSQL database.

## Project start up

### 1. Cloning the repository

```sh
git clone https://git.vegaitsourcing.rs/anita.pajic/to-do-list
cd to_do_list
```

### 2. Installing the requirements

```sh
pip install -r requirements.txt
```

### 3. Database config (PostgreSQL)

In `.env` file (create if not present) setup these variables:

```
DB_NAME=todolistdb
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply migrations

```sh
python manage.py migrate
```

### 6. Create superuser (optional, for admin panel)

```sh
python manage.py createsuperuser
```

### 7. Run server

```sh
python manage.py runserver
```

Application will be available on: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Additional commands

### Creation of new migrations

```sh
python manage.py makemigrations
```

## Project structure

```
TO-DO-LIST/
│── to_do_app/          # Main application
│   │── exceptions/
│   │── managers/
│   │── migrations/
│   │── models/
│   │── permissions/
│   │── serializers/
│   │── templates/
│   │── tests/
│   │── utils/
│   │── views/
│── to_do_project/      # Core project 
│   │── settings/
│   │── urls.p
│── manage.py           # Main managing file
│── .env                # Enviroment config
│── requirements.txt    # Dependency list
│── README.md 
```
