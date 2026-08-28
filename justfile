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

# Image built from .woodpecker/Dockerfile for the Woodpecker CI steps
ci_image := env_var_or_default("CI_IMAGE", "oci.atklab.cloud/enochecker-core/enochecker-core-ci")
ci_image_tag := env_var_or_default("CI_IMAGE_TAG", "latest")
ci_image_ref := ci_image + ":" + ci_image_tag

# Build the Woodpecker CI runner image
ci-image-build:
	docker build -f .woodpecker/Dockerfile -t {{ci_image_ref}} .

# Build and push the Woodpecker CI runner image
ci-image-push: ci-image-build
	docker push {{ci_image_ref}}
