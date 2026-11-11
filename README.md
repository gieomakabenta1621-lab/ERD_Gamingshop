# ERD Gaming Shop (Django)
Simple Django shop based on the supplied ERD.

## Install/run
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install django pillow
python manage.py makemigrations store
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ and admin at http://127.0.0.1:8000/admin/

## Use with an existing Django project
Copy `store/models.py`, `store/views.py`, `store/urls.py`, `store/admin.py`, `store/forms.py`, templates and static into your existing project.
Add `store` to `INSTALLED_APPS`, set `AUTH_USER_MODEL = "store.User"` **before your first migrations** if you want the ERD's base_users as custom user. If your existing database already has migrations/users, do not change AUTH_USER_MODEL; use Django's built-in User instead (this package's custom User then needs adapting).
