rebuild:
	rm -f dist/*
	poetry build --format wheel

mongo_test_up:
	docker compose -f docker-compose-dev.yml up -d

mongo_test_down:
	docker compose -f docker-compose-dev.yml down

run_tests:
	docker compose -f docker-compose-dev.yml up -d
	sleep 1
	poetry run pytest -v
	docker compose -f docker-compose-dev.yml down
