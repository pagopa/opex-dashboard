FROM python:3.9-slim

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
