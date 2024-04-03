# from https://hub.docker.com/_/python
FROM python:3.12.0-alpine3.17@sha256:d3f52543a68f2c98642a2efe3055d1c586d488b6d45e9dabea21c087b732f7f7 AS build

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
