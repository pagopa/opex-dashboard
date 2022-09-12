FROM python:3.9.14-alpine@sha256:d80bb38eb14230a70ef922956d0621f7dd938b16794057f6fe71a90ef9ec5504

RUN apk update && apk upgrade && apk add build-base
RUN pip install --upgrade pip

RUN adduser -D nonroot
USER nonroot
WORKDIR /home/nonroot

ENV PATH="/home/nonroot/.local/bin:${PATH}"

RUN pip install --user toml build

COPY --chown=nonroot:nonroot . .

RUN python -m build
RUN pip install dist/opex_dashboard*.whl

ENTRYPOINT ["opex_dashboard"]
