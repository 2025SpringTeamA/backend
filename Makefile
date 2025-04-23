up:
	docker compose up --build

up-d:
	docker compose up -d

ps:
	docker compose ps

logs:
	docker compose logs

exec-app:
	docker exec -it fastapi-app bash

exec-db:
	docker exec -it mysql-db bash

down:
	docker compose down

migrate:
	docker compose exec fastapi-app sh -c "cd /app && alembic upgrade head"

makemigration:
	@read -p "Migration name: " name; \
	docker compose exec fastapi-app sh -c "cd /app && alembic revision --autogenerate -m $$name"

show:
	docker compose exec fastapi-app sh -c "cd /app && alembic history"

downgrade:
	docker compose exec fastapi-app sh -c "cd /app && alembic downgrade -1"