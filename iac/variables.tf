variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "shinyan"
}

variable "location" {
  description = "Azure location where resources will be deployed"
  type        = string
  default     = "Australia East"
}

variable "storage_account_name" {
  description = "Name of the storage account"
  type        = string
  default     = "shinyastorage"
}

variable "openai_api_key" {
  description = "The value of the OpenAI API key."
  type        = string
  sensitive   = true
}