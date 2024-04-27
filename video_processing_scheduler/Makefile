include env.local

make run-local:
	set -a && . ./env.local && pipenv run main

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
