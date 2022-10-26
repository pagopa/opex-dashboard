# OpEx Dashboard

This is a tool to generate PagoPA's Operational Excellence dashboards from Open
Api specs.

## Usage

There are several way to use this tool. Each of them assume that the current
working directory stores the OA3 spec. The first step is to create a
configuration file:

```bash
cat <<EOF > config.yaml
oa3_spec: https://raw.githubusercontent.com/pagopa/opex-dashboard/main/test/data/io_backend.yaml
name: My dashboard
location: West Europe
timespan: 5m
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
  ghcr.io/pagopa/opex-dashboard:latest generate \
  --template-name azure-dashboard \
  --config-file -
```

`-` is a special value, it indicates stdin as input. Alternatively, it is always
possible to bind mount a volume and load the configuration file, as well as the
OA3 spec, from the volume:

```bash
docker run -v $(pwd):/home/nonroot/myfolder:Z \
  ghcr.io/pagopa/opex-dashboard:latest generate \
  --template-name azure-dashboard \
  --config-file myfolder/config.yaml
```

You can also load an OA3 spec by mounting it inside the container. In this case
you must pay attention to the path inside the `config.yaml`:

```yaml
oa3_spec: myfolder/oa3_spec.yaml
name: My dashboard
location: West Europe
timespan: 5m
resources:
  - /subscriptions/uuid/resourceGroups/my-rg/providers/Microsoft.Network/applicationGateways/my-gtw
EOF
```

### Build from local

There is a convenient (Dockerfile)[Dockerfile] that you can use to build the
image from scratch on your localhost.

```bash
git clone https://github.com/pagopa/opex-dashboard.git
```

```bash
cd opex-dashboard
```

```bash
docker build -t opexd .
```

### As a python library

Install the library:

```bash
git clone https://github.com/pagopa/opex-dashboard.git
```

```bash
cd opex-dashboard
```

```bash
pip install --user -e .
```

Create the dashboard:

```bash
opex_dashboard generate \
  --template-name azure-dashboard \
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
  --template-name azure-dashboard \
  --config-file config.yaml
```

### How to create a new template

This is a four steps process.

#### 1. Create the template

By using the [Django template
language](https://docs.djangoproject.com/en/4.1/ref/templates/language/),
create a new template in `src/opex_dashboard/template`. As example, consider
the following content for the file `src/opex_dashboard/template/mytemplate.json`:

```
{% load stringify mul %}
{
    "widgets": [
        {% for endpoint in endpoints %}
        {
            "height": 8,
            "width": 8,
            "x": 0,
            "y": {{ forloop.counter0|mul:8 }},
            "type": "log",
            "properties": {
                "query": "myquery#1",
                "region": "eu-south-1",
                "stacked": "false",
                "title": "Availability - {{endpoint}}",
                "view": "timeSeries"
            }
        },
        {
            "height": 8,
            "width": 8,
            "x": 8,
            "y": {{ forloop.counter0|mul:8 }},
            "type": "log",
            "properties": {
                "query": "myquery#2",
                "region": "eu-south-1",
                "stacked": "false",
                "title": "Response Codes - {{endpoint}}",
                "view": "timeSeries"
            }
        },
        {
            "height": 8,
            "width": 8,
            "x": 16,
            "y": {{ forloop.counter0|mul:8 }},
            "type": "log",
            "properties": {
                "query": "myquery#3",
                "region": "eu-south-1",
                "stacked": "false",
                "title": "Response time - {{endpoint}}",
                "view": "timeSeries"
            }
        }
        {% endfor %}
    ]
}
```

`stringy` and `mul` are custom tags. You can find their implementation in [tags
folder](https://github.com/pagopa/opex-dashboard/tree/main/src/opex_dashboard/tags).

#### 2. Create the builder

A builder is where you apply the business logic. There is a [base
Builder](https://github.com/pagopa/opex-dashboard/blob/main/src/opex_dashboard/builders/base.py)
you must inherit from. Consider the following builder, which takes an OA3 spec
to take all its endpoints:

```python
from typing import Dict, List, Any
from urllib.parse import urlparse

from opex_dashboard.builders.base import Builder
from opex_dashboard.resolver import OA3Resolver


class MyDashboardBuilder(Builder):
    _oa3_spec: Dict[str, Any]

    def __init__(self, resolver: OA3Resolver) -> None:
        """Create a MyDashbordBuilder object
        """
        self._oa3_spec = resolver.resolve()
        super().__init__(template="mytemplate.json")

    def produce(self, values: Dict[str, Any] = {}) -> str:
        """Render the template by merging base properties, given values, and information extracted form OA3 spec
        Returns:
            str: The rendered template
        """
        if "servers" in self._oa3_spec:
            self._properties["hosts"] = []
            self._properties["endpoints"] = []
            for server in self._oa3_spec["servers"]:
                url = urlparse(server["url"])
                self._properties["hosts"].append(url.netloc)
                for p in list(self._oa3_spec["paths"].keys()):
                    self._properties["endpoints"].append(f"{url.path}/{p[1:]}")
            self._properties["endpoints"] = [*set(self._properties["endpoints"])]
        else:
            base_path = self._oa3_spec["basePath"]
            self._properties["hosts"] = [self._oa3_spec["host"]]
            self._properties["endpoints"] = [f"{base_path}/{p[1:]}" for p in self._oa3_spec["paths"].keys()]

        return super().produce(values)
```

It must be save as `src/opex_dashboard/builders/my_dashboard_builder.py`.

#### 3. Enanche the builder factory

Modify `src/opex_dashboard/builder_factory.py` to create the new dashboard:

```python
# ...
from opex_dashboard.builders.my_dashboard_builder import MyDashboardBuilder
# ...
def create_my_builder(**args: Optional[Any]) -> Optional[Builder]:
    inputs = normalize_params(args, {
        "resolver": OA3Resolver,
        })
    return MyDashboardBuilder(**inputs)
# ...
def create_builder(template_type: str, **args: Optional[Any]) -> Optional[Builder]:
    # ...
    builders = {
      # ...
      "my-dashboard": create_my_builder,
      # ...
    }
    # ...
```

#### 4. Enanche the CLI

Update `src/opex_dashboard/commands/generate.py`:

```python
# ...
@click.option("--template-name", "-t",
              required=True,
              type=click.Choice([..., "my-dashboard"]),
              help="Name of the template.")
# ...
```

#### Testing

In the [test folder](https://github.com/pagopa/opex-dashboard/tree/main/test)
there are lots of tests, consider to upgrade it after develop a new template.
