FROM python:3.9.14-slim@sha256:d95dc32274f817debe886e6c5a6164bf4e0d996632d8cb56fde89189134db9d7

RUN pip install --upgrade pip

RUN useradd -m nonroot
USER nonroot
WORKDIR /home/nonroot

ENV PATH="/home/nonroot/.local/bin:${PATH}"

RUN pip install --user toml build

COPY --chown=nonroot:nonroot . .

RUN python -m build
RUN pip install dist/opex_dashboard*.whl

ENTRYPOINT ["opex_dashboard"]
