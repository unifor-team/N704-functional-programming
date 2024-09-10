# N704 - Programação Funcional

Using Flask to build a Restful API Server.

### Extension:
- Flask: [Flask](https://flask.palletsprojects.com/en/3.0.x/)

- Python-dotenv: [Dotenv](https://pypi.org/project/python-dotenv/)

- ORM: [Flask-Testing](https://pypi.org/project/psycopg2-binary/)

- Email Send: [secure-smtplib](https://pypi.org/project/secure-smtplib/)

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Flask Application Structure 
```
.
|────utils/
| |────email.py
| |────emailutils.py
| |────request.py
| |────response.py
|──────app.py
|──────query.py
|──────requirements.txt
|──────response_msg.py
|──────status_code.py
|──────.env.py
|──────.flaskenv.py
```


## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```
### Configuring From Files

#### Example Usage

```
app = Flask(__name__ )
app.config.from_pyfile('config.Development.cfg')
```

#### cfg example

##Flask settings
DEBUG = True  # True/False
TESTING = False

#### Builtin Configuration Values - .env

DATABASE_URL=URL

PORT=5000


### OAuth Setup
add your `client_id` and `client_secret` into config file.

### ESDAO Setup
add your `ES host` and `ES port` into config file 



 
## Run Flask
### Run flask for develop
```
$ flask run
```
In flask, Default port is `5000`

## Unittest
```
$ nosetests webapp/ --with-cov --cover-html --cover-package=app
```
- --with-cov : test with coverage
- --cover-html: coverage report in html format

