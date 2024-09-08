provider "azurerm" {
  features {}
}

resource "azurerm_cosmosdb_account" "cosmosdb_serverless" {
  name                = var.cosmosdb_account_name
  location            = var.location
  resource_group_name = var.resource_group_name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  enable_free_tier    = true
  capabilities {
    name = "EnableServerless"
  }
}

resource "azurerm_cosmosdb_sql_database" "database" {
  name                = var.database_name
  cosmosdb_account_id = azurerm_cosmosdb_account.cosmosdb_serverless.id
  resource_group_name = var.resource_group_name
}

resource "azurerm_cosmosdb_sql_container" "container" {
  name                = var.container_name
  cosmosdb_account_id = azurerm_cosmosdb_account.cosmosdb_serverless.id
  resource_group_name = var.resource_group_name
  database_name       = azurerm_cosmosdb_sql_database.database.name
  partition_key_path  = var.partition_key_path
}

# Assign the role to the Developers group for Cosmos DB
resource "azurerm_role_assignment" "developers_cosmosdb_role_assignment" {
  principal_id        = var.principal_id  # Accept the group ID as input to the module
  role_definition_name = "Cosmos DB Built-in Data Contributor"
  scope               = azurerm_cosmosdb_account.cosmosdb_serverless.id
}
