# OpEx Dashboard

This is a tool to generate PagoPA's Operational Excellence dashboards from Open
Api specs.

## Usage

There are several way to use this tool. Each of them assume that the current
working directory stores the OA3 spec. The first step is to create a
configuration file:

```bash
cat <<EOF > config.yaml
oa3_spec: https://raw.githubusercontent.com/pagopa/operational-excellence-dashboard/main/test/data/io_backend.yaml
name: My dashboard
location: West Europe
resources:
  - /subscriptions/uuid/resourceGroups/my-rg/providers/Microsoft.Network/applicationGateways/my-gtw
EOF
```

You can find practical example of configuration files in the [examples
folder](examples).

### Docker

This is the most convenient and rapid way. Generate the dashboard:

```bash
cat config.yaml | docker run -i \
  ghcr.io/pagopa/operational-excellence-dashboard:latest generate \
  --template-name azure-dashbaord \
  --config-file -
```

`-` is a special value, it indicates stdin as input. Alternatively, it is always
possible to bind mount a volume and load the configuration file, as well as the
OA3 spec, from the volume:

```bash
docker run -v $(pwd):/home/nonroot/resources:Z \
  ghcr.io/pagopa/operational-excellence-dashboard:latest generate \
  --template-name azure-dashbaord \
  --config-file home/nonroot/resources/config.yaml
```

### Build from local

There is a convenient (Dockerfile)[Dockerfile] that you can use to build the
image from scratch on your localhost.

```bash
git clone https://github.com/pagopa/operational-excellence-dashboard.git
```

```bash
cd operational-excellence-dashboard
```

```bash
docker build -t opexd .
```

### As a python library

Install the library:

```bash
git clone https://github.com/pagopa/operational-excellence-dashboard.git
```

```bash
cd operational-excellence-dashboard
```

```bash
pip install --user -e .
```

Create the dashboard:

```bash
opex_dashboard generate \
  --template-name azure-dashbaord \
  --config-file config.yaml
```

## Development

The development environment leverages on
[pipenv](https://pipenv.pypa.io/en/latest/).
[Pipfile](Pipfile) contains several convenient scripts to ease the development
process.

To set up your localhost:

```bash
pipenv install --dev
```

```bash
pipenv run install_local
```

```bash
pipenv run opex_dashboard generate \
  --template-name azure-dashbaord \
  --config-file config.yaml
```
