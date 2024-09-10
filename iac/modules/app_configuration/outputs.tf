output "app_configuration_id" {
  value = azurerm_app_configuration.this.id
}

output "identity_principal_id" {
  value = azurerm_app_configuration.this.identity[0].principal_id
}
