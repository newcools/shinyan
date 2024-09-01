variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "resource_group_id" {
  description = "Id of the resource group"
  type        = string
}

variable "location" {
  description = "Azure location where the App Configuration will be created"
  type        = string
}

variable "sku" {
  description = "price tier of the app configuration"
  type        = string
  default     = "free"
}
