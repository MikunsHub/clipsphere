COMPOSE_FILE=tests/docker-compose.yml

include env.local

docker-run:
	docker-compose -f ${COMPOSE_FILE} up -d

docker-clean:
	docker-compose -f ${COMPOSE_FILE} down

docker-respawn:
	docker rm -f postgres_container && docker-compose -f ${COMPOSE_FILE} up -d postgres

make run-local:
	set -a && . ./env.local && pipenv run dev

test:
	pipenv run lint
	pipenv run type-check
	set -a && . ./env.local && pipenv run test

quick-test:
	# Pass ISOLATED_TEST env var to run a single test f.e. tests/unit/test_centurion.py::test_fetch_recent_data
	set -a && . ./env.local && pipenv run test ${ISOLATED_TEST}

auto-format:
	pipenv run ruff-fix
	pipenv run ruff-format
	pipenv run ruff