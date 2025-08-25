.PHONY: help install install-dev test test-coverage lint format security clean pre-commit-install

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r Requirements.txt

install-dev: ## Install development dependencies
	pip install -r Requirements.txt
	pip install -r requirements-dev.txt

test: ## Run tests
	python manage.py test

test-coverage: ## Run tests with coverage
	coverage run --source='.' manage.py test
	coverage report --show-missing
	coverage html

lint: ## Run all linting checks
	@echo "Running flake8..."
	flake8 .
	@echo "Running black check..."
	black --check .
	@echo "Running isort check..."
	isort --check-only .
	@echo "Running mypy..."
	mypy . --ignore-missing-imports --exclude=migrations
	@echo "Running pylint..."
	pylint --load-plugins=pylint_django --django-settings-module=messaging_app.settings \
		--ignore=migrations,manage.py \
		--disable=C0114,C0115,C0116,R0903,W0613 \
		. || echo "Pylint completed with warnings"

format: ## Auto-format code
	black .
	isort .

security: ## Run security checks
	@echo "Running safety check..."
	safety check -r Requirements.txt
	@echo "Running bandit..."
	bandit -r . -x */migrations/*,*/venv/*,*/env/*,*/__pycache__/*
	@echo "Running semgrep..."
	semgrep --config=auto . || echo "Semgrep completed"

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf .mypy_cache
	rm -rf .pytest_cache

pre-commit-install: ## Install pre-commit hooks
	pre-commit install

migrate: ## Run Django migrations
	python manage.py makemigrations
	python manage.py migrate

runserver: ## Start Django development server
	python manage.py runserver

shell: ## Start Django shell
	python manage.py shell

collectstatic: ## Collect static files
	python manage.py collectstatic --noinput

ci-local: ## Run all CI checks locally
	@echo "🔍 Running local CI checks..."
	@echo "1. Installing dependencies..."
	@$(MAKE) install-dev
	@echo "2. Running tests with coverage..."
	@$(MAKE) test-coverage
	@echo "3. Running linting..."
	@$(MAKE) lint
	@echo "4. Running security checks..."
	@$(MAKE) security
	@echo "✅ All checks completed!"

# Docker commands
docker-build: ## Build Docker image locally
	docker build -t messaging-app:latest .

docker-run: ## Run Docker container locally
	docker run -d \
		--name messaging-app \
		-p 8000:8000 \
		-e DB_HOST=localhost \
		-e DB_PORT=3306 \
		-e DB_USER=django_user \
		-e DB_PASSWORD=django_password \
		-e DB_NAME=messaging_db \
		messaging-app:latest

docker-stop: ## Stop and remove Docker container
	docker stop messaging-app || true
	docker rm messaging-app || true

docker-logs: ## View Docker container logs
	docker logs -f messaging-app

docker-shell: ## Access Docker container shell
	docker exec -it messaging-app bash

docker-compose-up: ## Start services with docker-compose
	docker-compose -f docker-compose.prod.yml up -d

docker-compose-down: ## Stop services with docker-compose
	docker-compose -f docker-compose.prod.yml down

docker-compose-logs: ## View docker-compose logs
	docker-compose -f docker-compose.prod.yml logs -f

docker-health: ## Check Docker container health
	docker inspect --format='{{.State.Health.Status}}' messaging-app
