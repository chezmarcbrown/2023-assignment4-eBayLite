# 2023-assignment4-eBayLite

python -m venv venv 



.\venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
*optional* python manage.py createsuperuser
python manage.py runserver

*optional- create custom query objects* python manage.py shell

WHEN DONE WITH VENV
deactivate

```

