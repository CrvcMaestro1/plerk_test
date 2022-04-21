# How to deploy on heroku

Create app 
```
heroku create plerk-test-backend
```

Install postgres addon 
```
heroku addons:create heroku-postgresql:hobby-dev
```

Set enviroment variables

```
heroku config:set DISABLE_COLLECTSTATIC=1
heroku config:set ALLOWED_HOSTS=* plerk-test-backend.herokuapp.com
heroku config:set DEBUG=0
heroku config:set SECRET_KEY=YOUR_KEY
heroku config:set TIME_ZONE=America/Guayaquil
heroku config:set SSL_REQUIRED=1
```

Migrate and load fixtures
```
heroku run python manage.py migrate
heroku run python load_fixtures.py
```