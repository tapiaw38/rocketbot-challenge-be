API_SERVICE=rocketbot-challenge-api

# Application commands
build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f $(API_SERVICE)

clean:
	docker-compose down -v
	docker system prune -f

dev:
	docker-compose up --build

# Test commands
test-build:
	docker-compose -f docker-compose.test.yml build

test:
	docker-compose -f docker-compose.test.yml run --rm tests

test-verbose:
	docker-compose -f docker-compose.test.yml run --rm tests pytest -v

test-coverage:
	docker-compose -f docker-compose.test.yml run --rm tests pytest --cov=src --cov-report=html --cov-report=term

test-specific:
	docker-compose -f docker-compose.test.yml run --rm tests pytest $(TEST)

test-clean:
	docker-compose -f docker-compose.test.yml down --volumes --remove-orphans

# Development tools
format:
	black .
	isort .

lint:
	flake8 src tests
	mypy src

quality:
	make format
	make lint
	make test