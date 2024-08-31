variable "key_name" {
  description = "The name of the App Configuration key."
  type        = string
}

variable "app_configuration_id" {
  description = "The ID of the App Configuration instance."
  type        = string
}

variable "key" {
  description = "The key name to be created in App Configuration."
  type        = string
}

variable "value" {
  description = "The value of the key in App Configuration (in this case, the Key Vault URI)."
  type        = string
}
