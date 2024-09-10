provider "azurerm" {
  features {}
}

resource "azurerm_cosmosdb_account" "cosmosdb_serverless" {
  name                = var.cosmosdb_account_name
  location            = var.location
  resource_group_name = var.resource_group_name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  free_tier_enabled    = true
  capabilities {
    name = "EnableServerless"
  }

  # Add geo_location block
  geo_location {
    location          = var.location
    failover_priority = 0
  }

  consistency_policy {
    consistency_level = "Session"
  }
}

resource "azurerm_cosmosdb_sql_database" "database" {
  name                = var.database_name
  account_name        = var.cosmosdb_account_name
  resource_group_name = var.resource_group_name
}

resource "azurerm_cosmosdb_sql_container" "container" {
  name                = var.container_name
  account_name        = var.cosmosdb_account_name
  resource_group_name = var.resource_group_name
  database_name       = azurerm_cosmosdb_sql_database.database.name
  partition_key_paths   = [var.partition_key_path]
}

# Assign the role to the Developers group for Cosmos DB
# resource "azurerm_role_assignment" "developers_cosmosdb_role_assignment" {
#   principal_id        = var.principal_id
#   role_definition_name = "Cosmos DB Contributor"
#   scope               = azurerm_cosmosdb_account.cosmosdb_serverless.id
# }
