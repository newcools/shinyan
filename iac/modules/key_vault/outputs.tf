output "key_vault_id" {
  value = azurerm_key_vault.this.id
}

output "key_vault_name" {
  value = azurerm_key_vault.this.name
}

output "openai_api_key_reference" {
  value = azurerm_key_vault_secret.openai_api_key.versionless_id
}