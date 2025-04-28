coPD:
	conda activate PD

server:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

createsuperuser:
	python manage.py createsuperuser

clearcache:
	python manage.py cache_clear
