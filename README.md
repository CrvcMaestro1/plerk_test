# Plerk Backend Dev Test

# Run locally

### Create a locally database in postgres
### Install python 3
### Install requirements
`pip install -r requirements.txt`
### Migrate
`python manage.py migrate`
### Run load_fixtures.py file
`python load_fixtures.py`
### Execute tests
`pytest`
### Run
`python manage.py runserver`

# Run With Docker

### Start the project
    
Configure your .env as the example and run `docker-compose up`
    
### Execute tests
    
After build, run tests `docker-compose run --rm test`

# Deployed on heroku

https://plerk-test-backend.herokuapp.com

# DOCS

### Postman collection

https://documenter.getpostman.com/view/8486968/Uyr8nyMx


