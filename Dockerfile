FROM python:3.9.14-alpine@sha256:d80bb38eb14230a70ef922956d0621f7dd938b16794057f6fe71a90ef9ec5504 AS build

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
