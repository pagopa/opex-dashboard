terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "log_workspace_name" {
  description = "Name of the log analytics workspace"
  type        = string
}

variable "rg_name" {
  description = "Name of the resource group to deploy resources into"
  type        = string
}

variable "log_workspace_rg" {
  description = "Resource group of the log analytics workspace"
  type        = string
}

data "azurerm_log_analytics_workspace" "this" {
  name                = var.log_workspace_name
  resource_group_name = var.log_workspace_rg
}

resource "azurerm_resource_group" "this" {
  name     = var.rg_name
  location = "{{ location }}"
}

resource "azurerm_dashboard" "this" {
  name                = "{{ name }}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  dashboard_properties = <<-PROPS
    {{ dashboard_properties }}
  PROPS
}

{% for endpoint in endpoints %}
resource "azurerm_monitor_scheduled_query_rules_alert" "alarm_availability_{{ forloop.counter0 }}" {
  name                = replace(join("_",split("/", "Availability @ {{endpoint}}")), "/\\{|\\}/", "")
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  action {
    action_group = []
  }

  data_source_id          = data.azurerm_log_analytics_workspace.this.id
  description             = "Availability for {{endpoint}} is less than or equal to 99%"
  enabled                 = true
  auto_mitigation_enabled = false

  query = <<-QUERY
    {% include "queries/availability.kusto" with is_alarm=True %}
  QUERY

  severity    = 0
  frequency   = 10
  time_window = 20
  trigger {
    operator  = "GreaterThanOrEqual"
    threshold = 1
  }
}

resource "azurerm_monitor_scheduled_query_rules_alert" "alarm_time_{{ forloop.counter0 }}" {
  name                = replace(join("_",split("/", "ResponseTime @ {{endpoint}}")), "/\\{|\\}/", "")
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  action {
    action_group = []
  }

  data_source_id          = data.azurerm_log_analytics_workspace.this.id
  description             = "Response time for {{endpoint}} is less than or equal to 1s"
  enabled                 = true
  auto_mitigation_enabled = false

  query = <<-QUERY
    {% include "queries/response_time.kusto" with is_alarm=True %}
  QUERY

  severity    = 0
  frequency   = 10
  time_window = 20
  trigger {
    operator  = "GreaterThanOrEqual"
    threshold = 1
  }
}
{% endfor %}
