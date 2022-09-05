# OpEx Dashboard

This is a cli to generate PagoPA's Operational Excellence dashboards from open api specs

## Usage

```bash
$ docker run ...
```

### With Pipenv

```bash
$ pipenv run install_local
```

```bash
$ pipenv run opex_dashboard generate \
  --template-name azure-dashbaord \
  --az-oa3-spec path/to/oa3_spec.yaml \
  --az-name "Dashboard name" \
  --az-location "West Europe" \
  --az-resource "/subscriptions/uuid/resourceGroups/my-rg/providers/Microsoft.Network/applicationGateways/my-gtw"
```
