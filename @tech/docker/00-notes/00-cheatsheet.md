# Docker cheatsheet

## Images

```sh
docker build -t app:dev .           # build from the Dockerfile here
docker build --target build .       # stop at a named stage
docker images                       # local images and their sizes
docker history app:dev              # the layers and the instruction behind each
docker image prune                  # remove dangling images
```

## Containers

```sh
docker run --rm -it alpine sh       # throwaway interactive container
docker run -d --name web -p 8080:80 nginx
docker ps -a                        # every container, stopped ones included
docker logs -f web                  # follow output
docker exec -it web sh              # shell inside a running container
docker stop web                     # SIGTERM, then SIGKILL after 10 s
docker inspect web                  # everything, as JSON
docker stats                        # live CPU and memory per container
```

## Dockerfile practices

- Order instructions from least to most frequently changed: dependencies before
  source code, so a code change does not invalidate the dependency layer.
- Use multi-stage builds: compile in a fat image, ship from a slim or empty one. See
  [`01-snippets/00-multi-stage-build`](../01-snippets/00-multi-stage-build/).
- Pin base image versions. `latest` is a different image next month.
- Run as a non-root `USER`.
- Use the exec form, `ENTRYPOINT ["app"]`, so the process is PID 1 and receives
  signals. The shell form wraps it in `/bin/sh -c`, which does not forward them.
- Keep a `.dockerignore` so `.git`, `node_modules` and secrets never reach the build
  context.

## Volumes and networks

```sh
docker volume create data
docker run -v data:/var/lib/data app        # named volume, managed by Docker
docker run -v "$PWD":/src app               # bind mount of the current directory
docker network create backend
docker run --network backend --name db postgres   # reachable as "db" on that network
```

## Compose

```sh
docker compose up -d --wait         # start and wait for healthchecks
docker compose ps
docker compose logs -f service
docker compose exec service sh
docker compose down --volumes       # stop, remove containers, networks and volumes
```

## Under the hood

A container is a process with namespaces (what it can see: pid, net, mnt, uts, ipc,
user) and cgroups (what it can use: CPU, memory, IO). An image is a stack of
read-only layers with one writable layer added on top at run time.
