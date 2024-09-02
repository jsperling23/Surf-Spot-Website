build: 
	docker-compose up -d --build

up:
	docker-compose up -d

down:
	docker-compose down

.PHONY: up down build
