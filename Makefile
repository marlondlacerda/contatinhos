i-dev:
	pip install -r dev-requirements.txt

install:
	pip install -r requirements.txt

superuser:
	bash -c "cd src && python manage.py createsuperuser"

makemigration:
	bash -c "cd src && python manage.py makemigrations"

migrate:
	bash -c "cd src && python manage.py migrate"

seeder:
	bash -c "cd src/contatos/seeders && python 0001_contatos_seed.py"

run:
	bash -c "cd src && python manage.py runserver"
