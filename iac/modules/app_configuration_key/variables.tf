variable "keys_map" {
  description = "A map of keys and their corresponding Key Vault secret URIs to be stored in the App Configuration."
  type        = map(string)
}

variable "app_configuration_id" {
  description = "The ID of the App Configuration instance."
  type        = string
}

variable "key_vault_id" {
  description = "The ID of the Key Vault."
  type        = string
}

variable "app_configuration_identity" {
  description = "The object ID of the managed identity assigned to the App Configuration."
  type        = string
}