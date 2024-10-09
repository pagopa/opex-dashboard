{% load stringify add_str %}
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
  name                = replace(join("_",split("/", "${local.name}-availability @ {{base_path|default:""|add_str:endpoint}}")), "/\\{|\\}/", "")
  resource_group_name = data.azurerm_resource_group.this.name
  location            = data.azurerm_resource_group.this.location

  action {
    action_group = {{ action_groups_ids|stringify }}
  }

  data_source_id          = "{{ data_source_id }}"
  description             = "Availability for {{base_path|default:""|add_str:endpoint}} is less than or equal to 99% - ${local.dashboard_base_addr}${azurerm_portal_dashboard.this.id}"
  enabled                 = true
  auto_mitigation_enabled = false

  query = <<-QUERY
{% with resource_type|add_str:"_queries/availability.kusto" as query %}
    {% include query with is_alarm=True threshold=props.availability_threshold %}
{% endwith %}
  QUERY

  severity    = 1
  frequency   = {{ props.availability_evaluation_frequency }}
  time_window = {{ props.availability_evaluation_time_window }}
  trigger {
    operator  = "GreaterThanOrEqual"
    threshold = {{ props.availability_event_occurrences }}
  }

  tags = var.tags
}

resource "azurerm_monitor_scheduled_query_rules_alert" "alarm_time_{{ forloop.counter0 }}" {
  name                = replace(join("_",split("/", "${local.name}-responsetime @ {{base_path|default:""|add_str:endpoint}}")), "/\\{|\\}/", "")
  resource_group_name = data.azurerm_resource_group.this.name
  location            = data.azurerm_resource_group.this.location

  action {
    action_group = {{ action_groups_ids|stringify }}
  }

  data_source_id          = "{{ data_source_id }}"
  description             = "Response time for {{base_path|default:""|add_str:endpoint}} is less than or equal to 1s - ${local.dashboard_base_addr}${azurerm_portal_dashboard.this.id}"
  enabled                 = true
  auto_mitigation_enabled = false

  query = <<-QUERY
{% with resource_type|add_str:"_queries/response_time.kusto" as query %}
    {% include query with is_alarm=True threshold=props.response_time_threshold %}
{% endwith %}
  QUERY

  severity    = 1
  frequency   = {{ props.response_time_evaluation_frequency }}
  time_window = {{ props.response_time_evaluation_time_window }}
  trigger {
    operator  = "GreaterThanOrEqual"
    threshold = {{ props.response_time_event_occurrences }}
  }

  tags = var.tags
}
{% endfor %}
