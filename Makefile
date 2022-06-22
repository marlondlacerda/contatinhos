#  <--------- Install Required Packages ---------->
idev:
	pip install -r dev-requirements.txt
install:
	pip install -r requirements.txt

#  <--------- Start Server ---------->
run:
	bash -c "cd app && python manage.py runserver"

# <--------- Create New App ---------->
newapp:
	bash -c "cd app && python manage.py startapp $(app)"

# <---------Run Lint ---------->
lint:
	flake8 app/

# <---------Commands for Database ---------->
superuser:
	bash -c "cd app && python manage.py createsuperuser"

resetdb:
	bash -c "cd app && python manage.py flush --noinput"

migration:
	bash -c "cd app && python manage.py makemigrations"

migrate:
	bash -c "cd app && python manage.py migrate"

seeder:
	bash -c "cd app/contatos/seeders && python 0001_contatos_seed.py"
