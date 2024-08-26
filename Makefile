INIT_FILE = .init_done

all: migrate up

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

re: down up

migrate: $(INIT_FILE)

$(INIT_FILE):
	docker-compose up -d
	docker exec web_room python3 manage.py makemigrations
	docker exec web_room python3 manage.py migrate
	touch $(INIT_FILE)
