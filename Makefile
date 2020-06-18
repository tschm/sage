#!make
PROJECT_VERSION := 0.1.1
SHELL := /bin/bash


.PHONY: help build test jupyter tag


.DEFAULT: help

help:
	@echo "make build"
	@echo "       Build the docker image."
	@echo "make jupyter"
	@echo "       Start the Jupyter server."
	@echo "make tag"
	@echo "       Make a tag on Github."
	@echo "make hub"
	@echo "       Push Docker Image to DockerHub."

build:
	docker-compose build jupyter

test:
	docker-compose -f docker-compose.test.yml run sut

jupyter: build
	echo "http://localhost:8888"
	docker-compose up jupyter

tag:
	git tag -a ${PROJECT_VERSION} -m "new tag"
	git push --tags


