variable "prefix" {
  type    = string
  validation {
    condition = (
      length(var.prefix) <= 6
    )
    error_message = "Max length is 6 chars."
  }
}

variable "env" {
  type = string
  validation {
    condition = (
      length(var.env) <= 3
    )
    error_message = "Max length is 3 chars."
  }
}

variable "env_short" {
  type = string
  validation {
    condition = (
      length(var.env_short) <= 1
    )
    error_message = "Max length is 1 chars."
  }
}

variable "location" {
  type    = string
}

variable "location_short" {
  description = "Location short like eg: neu, weu.."
  type        = string
}

variable "tags" {
  type = map(any)
  default = {
    CreatedBy = "Terraform"
  }
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

