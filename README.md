# Approach

Due to the nature of the assigment I have decided to use Django REST framework with sqllite3. 


# How to run the server

Use python3 
```
git clone git@github.com:jonasanso/surveys.git
cd surveys
python -m venv env
source env/bin/activate
pip install django
pip install djangorestframework
python manage.py migrate
python manage.py runserver
```

# How to use the API
Open http://127.0.0.1:8000/ and you will see django debug error detailing the routes.
Inside test_views you can find all the requests for everyone of the requirements

# Assumptions
- Available places can be any whone number including zero limited to integers

# Had I had more time, I would
- Add more unit tests
- Add more integration tests
- Document API
- Use transactions

# Outside of scope improvements
- Do not user sqllite3
- Do not use INTEGER for the ids and not use autoincrement in production


