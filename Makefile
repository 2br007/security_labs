lab:
	docker-compose down
	docker-compose up --build -d

down:
	docker-compose down

test:
	docker-compose exec app pytest -q

install:
	pip install -r requirements.txt

check:
	pre-commit run --all-files