API_SERVICE=rocketbot-challenge-api

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f $(API_SERVICE)

docker-clean:
	docker-compose down -v
	docker system prune -f

run-dev:
	docker-compose up --build