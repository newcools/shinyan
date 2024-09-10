# Retrieve the current user's details
data "azurerm_client_config" "current" {}

# Define the storage account
resource "azurerm_storage_account" "this" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "Terraform"
  }
}

# Define the default storage container
resource "azurerm_storage_container" "default" {
  name                  = var.container_name
  storage_account_name  = azurerm_storage_account.this.name
  container_access_type = "private"
}


# # Assign the "Storage Blob Data Contributor" role to the current user for the storage account
# resource "azurerm_role_assignment" "current_user_blob_data_contributor" {
#   scope                = azurerm_storage_account.this.id
#   role_definition_name = "Storage Blob Data Contributor"
#   principal_id         = data.azurerm_client_config.current.object_id
# }