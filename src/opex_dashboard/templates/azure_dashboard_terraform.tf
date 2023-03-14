{% load stringify %}
locals {
  name                = "${var.prefix}-${var.env_short}-{{name}}"
  dashboard_base_addr = "https://portal.azure.com/#@pagopait.onmicrosoft.com/dashboard/arm"
}

data "azurerm_resource_group" "this" {
  name     = "dashboards"
}

resource "azurerm_portal_dashboard" "this" {
  name                = local.name
  resource_group_name = data.azurerm_resource_group.this.name
  location            = data.azurerm_resource_group.this.location

  dashboard_properties = <<-PROPS
    {{ dashboard_properties }}
  PROPS

  tags = var.tags
}

{% for endpoint,props in endpoints.items %}
resource "azurerm_monitor_scheduled_query_rules_alert" "alarm_availability_{{ forloop.counter0 }}" {
  name                = replace(join("_",split("/", "${local.name}-availability @ {{endpoint}}")), "/\\{|\\}/", "")
  resource_group_name = data.azurerm_resource_group.this.name
  location            = data.azurerm_resource_group.this.location

  action {
    action_group = {{ action_groups_ids|stringify }}
  }

  data_source_id          = "{{ data_source_id }}"
  description             = "Availability for {{endpoint}} is less than or equal to 99% - ${local.dashboard_base_addr}${azurerm_portal_dashboard.this.id}"
  enabled                 = true
  auto_mitigation_enabled = false

  {% if resource_type == 'app-gateway' %}
  query = <<-QUERY
    {% include "gateway_queries/availability.kusto" with is_alarm=True threshold=props.availability_threshold %}
  QUERY
  {% else %}
  query = <<-QUERY
    {% include "apim_queries/availability.kusto" with is_alarm=True threshold=props.availability_threshold %}
  QUERY
  {% endif %}

  severity    = 1
  frequency   = 10
  time_window = 20
  trigger {
    operator  = "GreaterThanOrEqual"
    threshold = 1
  }

  tags = var.tags
}

resource "azurerm_monitor_scheduled_query_rules_alert" "alarm_time_{{ forloop.counter0 }}" {
  name                = replace(join("_",split("/", "${local.name}-responsetime @ {{endpoint}}")), "/\\{|\\}/", "")
  resource_group_name = data.azurerm_resource_group.this.name
  location            = data.azurerm_resource_group.this.location

  action {
    action_group = {{ action_groups_ids|stringify }}
  }

  data_source_id          = "{{ data_source_id }}"
  description             = "Response time for {{endpoint}} is less than or equal to 1s - ${local.dashboard_base_addr}${azurerm_portal_dashboard.this.id}"
  enabled                 = true
  auto_mitigation_enabled = false

  {% if resource_type == 'app-gateway' %}
  query = <<-QUERY
    {% include "gateway_queries/response_time.kusto" with is_alarm=True threshold=props.response_time_threshold %}
  QUERY
  {% else %}
  query = <<-QUERY
    {% include "apim_queries/response_time.kusto" with is_alarm=True threshold=props.response_time_threshold %}
  QUERY
  {% endif %}

  severity    = 1
  frequency   = 10
  time_window = 20
  trigger {
    operator  = "GreaterThanOrEqual"
    threshold = 1
  }

  tags = var.tags
}
{% endfor %}
