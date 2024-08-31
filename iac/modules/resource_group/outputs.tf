output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "location" {
  value = azurerm_resource_group.this.location
}

output "resource_group_id" {
  value = azurerm_resource_group.this.id
}