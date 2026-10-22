# Multi-stage build

How do I ship a compiled program without shipping the compiler?

## Run

```sh
make run
make test
```

Needs Docker.

## What to notice

- The first stage carries the whole Go toolchain. The second starts `FROM scratch`, an
  image with zero files, and copies in only the binary. The final image is a couple of
  megabytes; the test fails if it ever grows past 5 MB.
- `CGO_ENABLED=0` matters: a dynamically linked binary would look for a libc that
  `scratch` does not have, and die with a confusing "no such file or directory".
- There is no shell inside, so there is nothing to `docker exec` into. The test proves it,
  and it is also a smaller attack surface.
- `USER 65534:65534` (nobody) runs it unprivileged. `scratch` has no `/etc/passwd`, so
  the user is given as numbers, not a name.
