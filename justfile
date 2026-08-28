uv_flags := env_var_or_default("UV_FLAGS", "--inexact")
uv_run := "env VIRTUAL_ENV=.venv uv run " + uv_flags

all: format lint mypy test

fix: format-fix lint-fix

format:
	@{{uv_run}} --group dev ruff format --check

format-fix:
	@{{uv_run}} --group dev ruff format

lint:
	@{{uv_run}} --group dev ruff check

lint-fix:
	@{{uv_run}} --group dev ruff check --fix

mypy:
	@{{uv_run}} --group dev mypy src/enochecker_core

build:
	@uv build

test:
	#!/usr/bin/env sh
	set -eu
	if [ -n "$(ls tests 2>/dev/null)" ]; then
		{{uv_run}} --group dev pytest -v
	fi
