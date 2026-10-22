# Stage 1: the full Go toolchain, roughly 250 MB, used only to compile.
FROM golang:1.25-alpine AS build
WORKDIR /src
COPY main.go .
# Static binary (no libc to link against in the final image), symbols stripped.
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /hello main.go

# Stage 2: nothing at all. Only the binary is copied over.
FROM scratch
COPY --from=build /hello /hello
USER 65534:65534
ENTRYPOINT ["/hello"]
