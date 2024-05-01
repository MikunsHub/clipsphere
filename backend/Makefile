COMPOSE_FILE=docker-compose.yml
SHARED_FOLDER := $(shell dirname "$(realpath $(lastword $(MAKEFILE_LIST)))")/../shared
BACKEND_SHARED_FOLDER := $(shell dirname "$(realpath $(lastword $(MAKEFILE_LIST)))")/shared

include env.local

docker-run:
	docker-compose -f ${COMPOSE_FILE} up -d
	sleep 3
	awslocal s3api create-bucket --bucket raw-videos-storage-bucket

docker-clean:
	docker-compose -f ${COMPOSE_FILE} down

docker-respawn:
	docker rm -f postgres_container && docker-compose -f ${COMPOSE_FILE} up -d postgres

copy-shared:
	@rm -rf ""$(BACKEND_SHARED_FOLDER)""
	@cp -R "$(SHARED_FOLDER)" "$(BACKEND_SHARED_FOLDER)" && \
	echo "Shared module copied to backend project..." && \
	echo "\033[0;31mWARNING\033[0m: DO NOT EDIT THE COPIED SHARED FOLDER DIRECTLY!!, THIS DELETES ON EVERY RESTART!!" \

run-local:
	$(MAKE) copy-shared
	set -a && . ./env.local && pipenv run dev

migrate:
	set -a	&& . ./env.local && pipenv run head

upgrade:
	set -a	&& . ./env.local && pipenv run upgrade

downgrade:
	set -a	&& . ./env.local && pipenv run downgrade

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
