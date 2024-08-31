output "app_configuration_keys" {
  description = "The IDs of the App Configuration keys created"
  value       = { for key, config in azurerm_app_configuration_key.this : key => config.id }
}

output "app_configuration_key_values" {
  description = "The values of the App Configuration keys created"
  value       = { for key, config in azurerm_app_configuration_key.this : key => config.value }
}
