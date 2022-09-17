# Vending Machine App

This is python-django based machine vending backend with DRF(Django RestFull API), SQLite database and basic OAuth2 authentication

## Setup

1. clone this project and navigate to the project folder

2. activate the environment

   ```sh
   source env/bin/activate
   ```

3. install requirements
   ```sh
   pip install -r requirements.txt
   ```
4. create .env file in the vending_machine folder, generate secret key by running the command below

   ```py
   python -c 'from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())'
   ```

   copy the key from termal and in .env file add SECRET_KEY='PASTE_YOUR_KEY_HERE'

5. make migrations and migrate
   ```py
   python manage.py makemigrations
   python manage.py migrate
   ```
6. create super admin and fill in the prompts
   ```py
   python manage.py createsuperuser
   ```
7. run server at port 8000
   ```py
   python manage.py runserver 8000
   ```

## API Collections

The api collections are in the vendor_machine_collection.json file
