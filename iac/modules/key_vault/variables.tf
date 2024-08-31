variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure location where the Key Vault will be created"
  type        = string
}

variable "tenant_id" {
  description = "Tenant ID for the Azure subscription"
  type        = string
}

variable "object_id" {
  description = "Object ID for the Azure client"
  type        = string
}

variable "openai_api_key" {
  description = "The value of the open AI api key."
  type        = string
  sensitive   = true
}
