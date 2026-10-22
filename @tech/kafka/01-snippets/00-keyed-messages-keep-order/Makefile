export COMPOSE_PROJECT_NAME := sandbox-kafka-keyed-messages

.PHONY: up down run test

up:
	docker compose up --detach --wait --quiet-pull

down:
	docker compose down --volumes

run: up
	bash demo.sh; status=$$?; $(MAKE) down; exit $$status

test: up
	bash demo.sh | bash check.sh; status=$$?; $(MAKE) down; exit $$status
