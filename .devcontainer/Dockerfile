FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# The workspace is mounted from the host, so uv will always have to copy files
# across file systems.
ENV UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:0.7.19 /uv /uvx /bin/
