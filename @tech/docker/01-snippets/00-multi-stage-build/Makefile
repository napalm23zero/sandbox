IMAGE := sandbox/docker-multi-stage-build
MAX_BYTES := 5000000

.PHONY: build run test clean

build:
	docker build --quiet --tag $(IMAGE) . >/dev/null

run: build
	docker run --rm $(IMAGE)
	@docker image inspect --format 'image size: {{.Size}} bytes' $(IMAGE)

test: build
	docker run --rm $(IMAGE) | grep -q "in an empty image"
	test $$(docker image inspect --format '{{.Size}}' $(IMAGE)) -lt $(MAX_BYTES)
	test "$$(docker image inspect --format '{{.Config.User}}' $(IMAGE))" = "65534:65534"
	! docker run --rm --entrypoint /bin/sh $(IMAGE) -c true 2>/dev/null
	@echo ok

clean:
	docker image rm $(IMAGE)
