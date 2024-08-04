output "storage_account_id" {
  value = azurerm_storage_account.this.id
}

output "blob_container_id" {
  value = azurerm_storage_container.this.id
}