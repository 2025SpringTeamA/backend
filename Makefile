up:
	docker compose up --build

up-d:
	docker compose up -d

ps:
	docker compose ps

logs:
	docker compose logs

exec-app:
	docker compose exec -it web bash

exec-db:
	docker compose exec -it db bash

db-shell:
	docker compose exec -it db bash -c "mysql -u root -p"

down:
	docker compose down

migrate:
	docker compose exec -it web bash -c "cd /app && alembic upgrade head"

makemigration:
	@read -p "Migration name: " name; \
	docker compose exec -it web bash -c "cd /app && alembic revision --autogenerate -m $$name"

show:
	docker compose exec -it web bash -c "cd /app && alembic history"

downgrade:
	docker compose exec -it web bash -c "cd /app && alembic downgrade -1"
