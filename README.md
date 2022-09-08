# OpEx Dashboard

This is a tool to generate PagoPA's Operational Excellence dashboards from open api specs

## Usage

Assuming specs are in the current workdir:

```bash
docker run -v /path/to/spec.yaml:/home/nonroot/spec.yaml:Z \
  ghcr.io/pagopa/operational-excellence-dashboard:latest generate \
  --template-name azure-dashbaord \
  --az-oa3-spec home/nonroot/spec.yaml \
  --az-name "Dashboard name" \
  --az-location "West Europe" \
  --az-resource "/subscriptions/uuid/resourceGroups/my-rg/providers/Microsoft.Network/applicationGateways/my-gtw"
```

### Build from local

```bash
git clone https://github.com/pagopa/operational-excellence-dashboard.git
```

```bash
cd operational-excellence-dashboard
```

```bash
docker build -t opexd .
```

```bash
docker run -v /path/to/spec.yaml:/home/nonroot/spec.yaml:Z \
  opexd generate \
  --template-name azure-dashbaord \
  --az-oa3-spec home/nonroot/spec.yaml \
  --az-name "Dashboard name" \
  --az-location "West Europe" \
  --az-resource "/subscriptions/uuid/resourceGroups/my-rg/providers/Microsoft.Network/applicationGateways/my-gtw"
```

## Development

```bash
pipenv install --dev
```

```bash
pipenv run install_local
```

```bash
pipenv run opex_dashboard generate \
  --template-name azure-dashbaord \
  --az-oa3-spec path/to/oa3_spec.yaml \
  --az-name "Dashboard name" \
  --az-location "West Europe" \
  --az-resource "/subscriptions/uuid/resourceGroups/my-rg/providers/Microsoft.Network/applicationGateways/my-gtw"
```
