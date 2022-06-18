#  <--------- Install Required Packages ---------->
idev:
	pip install -r dev-requirements.txt
install:
	pip install -r requirements.txt

#  <--------- Start Server ---------->
run:
	bash -c "cd src && python manage.py runserver"

# <--------- Create New App ---------->
newapp:
	bash -c "cd src && python manage.py startapp $(app)"

# <---------Run Lint ---------->
lint:
	flake8 src/

# <---------Commands for Database ---------->
superuser:
	bash -c "cd src && python manage.py createsuperuser"

resetdb:
	bash -c "cd src && python manage.py flush --noinput"

migration:
	bash -c "cd src && python manage.py makemigrations"

migrate:
	bash -c "cd src && python manage.py migrate"

seeder:
	bash -c "cd src/contatos/seeders && python 0001_contatos_seed.py"
