# FoodService (Test Task)
API service for management of food service written on DRF

```shell
git clone https://github.com/LaskoA/FoodService
cd FoodService

Virtual environment install for Windows:
  - python3 -m venv venv
  - venv\Scripts\activate
  - pip install -r requirements.txt
  
Virtual environment install for Mac:
  - sudo pip install virtualenv
  - virtualenv env
  - source env/bin/activate


python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py loaddata printers.json
```

## Description of endpoints
- http://127.0.0.1:8000/admin/ - admin page with filtering for Check Model
- http://127.0.0.1:8000/app/orders/ - dummy list with orders
- http://127.0.0.1:8000/app/create-check/ - creates checks
- http://127.0.0.1:8000/app/print-check/ - prints checks
- http://127.0.0.1:8000/app/printers/ - full CRUD for printers
- http://127.0.0.1:8000/app/checks/ - full CRUD for checks

Detailed swagger info is available here: http://127.0.0.1:8000/api/doc/swagger/ and here: http://127.0.0.1:8000/api/doc/redoc/

## Notes 
- in views.py please replace "path_wkhtmltopdf" to relevant for your PC
- superuser with login "admin" and password "admin12345" was created
- don`t forget to run 'python manage.py loaddata printers.json' to get list of printers for test
