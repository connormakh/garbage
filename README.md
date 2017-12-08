# Garbage

### Installation:

_Clone this repository_:
```sh
$ git clone https://github.com/connormakh/garbage.git
```

Create a virtual environment to run this project in an isolated python3 container
```sh
$ virtualenv garbage-env
```

If you don't have Autoenv, install it globally, outside of your virtual env:
```sh
$ pip install autoenv
```

Create a .env file to automatically load your virtual environment whenever you `cd` into it. Add the following to your .env file:
```
source bin/activate
export FLASK_APP="garbage/run.py"
export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
export APP_SETTINGS="development"
export DATABASE_URL="postgresql://localhost/garbage-db"
```
*Make sure to source your .env code once done*:
```sh
$ source .env
```

### Vars
Create a instance/vars.py file, with the following:
```py
FLASK_APP="garbage-backend/run.py"
SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
APP_SETTINGS="development"
DATABASE_URL="postgresql://localhost/garbage-db"
MONGO_URL="mongodb://localhost/garbage-db"
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=587
MAIL_PASSWORD="********"
MAIL_USERNAME="garbagemanlau@gmail.com"

```

### Dependancies:
Install dependancies using pip:
```sh
$ pip install -r requirements.txt
```


### Database:

This project uses postgreSQL, so make sure you have that on your machine before moving forward.

Initialize the database:

```sh
$ createdb garbage-db
```

Migrate and upgrade your database:
```sh
$ python3 manage.py db init
$ python3 manage.py db migrate
$ python3 manage.py db upgrade
```

### Tests

 ...TODO


