variable "keys_map" {
  description = "A map of keys and their corresponding Key Vault secret URIs to be stored in the App Configuration."
  type        = map(string)
}

variable "app_configuration_id" {
  description = "The ID of the App Configuration instance."
  type        = string
}