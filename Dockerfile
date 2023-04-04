# from https://hub.docker.com/_/python
FROM python:3.11.2-alpine3.17@sha256:1c66f5282876229c87851cde3a1c7eb8939f212cdf398201f86f5416c7907656 AS build

ARG user=nonroot

ENV PATH="/home/${user}/.local/bin:${PATH}"

RUN \
  apk update && \
  apk upgrade && \
  apk add build-base && \
  rm -rf /var/cache/apk/* && \
  adduser -D ${user}

USER ${user}
WORKDIR /home/${user}

COPY --chown=${user} . .
RUN \
  pip install toml build && \
  python -m build && \
  pip install dist/opex_dashboard*.whl && \
  pip cache purge && \
  rm -fr dist

ENTRYPOINT ["opex_dashboard"]
