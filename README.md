# Fake CSV Generator

### Local testing

Install python 3.6+, Redis

Execute in terminal:
```bash
virtualenv -p python3.6 env
source env/bin/activate
pip install -r requirements.txt
```

Initialize DB tables:

```bash
python manage.py makemigrations
python manage.py runserver
```

To run django development server:

```bash
python manage.py runserver
```