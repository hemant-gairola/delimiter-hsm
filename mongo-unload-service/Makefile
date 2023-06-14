#
# Copyright (c) 2022 by Delphix. All rights reserved.
#
.PHONY: --check_python --check_env_exists run tests --create_virtual_env --install_dependencies env clean_build clean_env clean build install version docker-image docker-run docker-stop docker-rm

ROOT_DIR := $(shell pwd)
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
red := $(shell tput setaf 1)
reset := $(shell tput sgr0)
SITE_PACKAGE_PATH := $(VENV)/lib/python3.9/site-packages
REPO := https://artifactory.delphix.com/artifactory/api/pypi/delphix-local
DOCKER_CONTAINER_NAME := mongo-hsc-unload-container
DOCKER_IMAGE_NAME := mongo-hsc-unload-image

define check_python_exists
	@if ! command -v python3.9 -V >/dev/null 2>&1; then \
		echo "Python 3.9 is NOT present on the system, Please install it"; \
		exit 1; \
	fi
endef

define show_version
	@export LC_ALL=en_AU.UTF-8; $(SDM) --version
endef

version:
	@# Help: Shows the version of the sdm binary
	@$(call show_version);

--check_python:
	@# Help: Checks existence of python virtual environment
	$(call check_python_exists)

--check_env_exists: --check_python
	@[ -f $(PYTHON) ] && echo $(PYTHON) exists || (echo $(PYTHON) does NOT exist, use \"make env\" to create a virtual env; exit 1)


run: --check_env_exists --export_lang
	@# Help: Runs the Fast API server on port 8080 using uvicorn
	-@echo 'Running the app...'
	-$(UVICORN) src.main:app --host 0.0.0.0 --port 8080 --reload

install: run
	@# Help: Installs sdm as an editable package inside python virtual environment
	-@echo 'Installing sdm with --editable mode using pip'
	@$(PIP) install -e .

tests:
	@# Help: Runs the unit tests inside tests folder and create a report
	$(PYTHON) -m pytest tests -s -v

--create_virtual_env: --check_python
	@# Help: Creates a virtual environment
	-@echo 'Creating Virtual environment'
	@python3.9 -m venv venv || echo 'Python env already exists'

--install_dependencies: requirements.txt
	@# Help: Installs the dependencies from requirements.txt
	-@echo 'Installing Dependencies...'
	@$(PYTHON) -m pip install --upgrade pip
	@$(PIP) install -r requirements.txt --no-cache-dir

env: --create_virtual_env --install_dependencies
	@# Help: Creates a virtual environment with python3.9 if not already present and activates it
	-@echo "Attaching pre commit";
	-@$(VENV)/bin/pre-commit install

clean_env:
	@# Help: Clean the virtual env that was created
	-@$(VENV)/bin/pre-commit uninstall
	-@rm -rf venv

clean_build:
	@# Help: Cleans the build files
	-@rm -rf build/
	-@rm -rf dist/
	-@rm -f sdm.spec

clean: clean_build
	@# Help: Cleans the pycache, coverage and build files
	-@rm -rf __pycache__
	-@rm -f .coverage
	-@rm -rf tests/.pytest_cache
	-@rm -rf tests/CodeCoverage
	-@rm -rf tests/Report.html
	-@rm -rf sdm.egg-info

docker-image:
	@# Help: Creates the docker image
	-@docker build -t $(DOCKER_IMAGE_NAME) .

docker-run:
	@# Help: Runs the docker container using the created image
	-@docker run -d -p 8082:8080 --name mongo-hsc-unload-container mongo-hsc-unload-image
	-@echo "The mongo-unload-hsc-container swagger UI can be accessed at http://0.0.0.0:8082"

docker-stop:
	@# Help: Stops the docker container
	-@docker stop $(DOCKER_CONTAINER_NAME)
	-@echo Stopped the container

docker-rm: docker-stop
	@# Help: Removes the docker container
	-@docker rm $(DOCKER_CONTAINER_NAME)
	-@echo Removed the container

--export_lang:
	LC_ALL=en_AU.UTF-8
	PYTHONPATH=$(ROOT_DIR)
	@export LC_ALL
	@export PYTHONPATH
	-@echo 'All env variables exported'


# A hidden target
.hidden:
help:
	@printf "%-20s %s\n" "Target" "Description"
	@printf "%-20s %s\n" "------" "-----------"
	@make -pqR : 2>/dev/null \
        | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' \
        | sort \
        | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' \
        | xargs -I _ sh -c 'printf "%-20s " _; make _ -nB | (grep -i "^# Help:" || echo "") | tail -1 | sed "s/^# Help: //g"'