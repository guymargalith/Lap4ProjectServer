web: gunicorn backend.wsgi --log-file -
heroku ps:scale web=1 
heroku config:set DISABLE_COLLECTSTATIC=1
heroku python manage.py migrate

