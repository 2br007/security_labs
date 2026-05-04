lab:
	docker-compose down
	docker-compose up --build -d

down:
	docker-compose down -v

test:
	docker-compose run --rm app pytest -q

install:
	pip install -r requirements.txt

check:
	pre-commit run --all-files