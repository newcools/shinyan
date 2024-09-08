output "cosmosdb_account_id" {
  description = "The ID of the Cosmos DB account."
  value       = azurerm_cosmosdb_account.cosmosdb_serverless.id
}

output "cosmosdb_database_name" {
  description = "The name of the Cosmos DB database."
  value       = azurerm_cosmosdb_sql_database.database.name
}

output "cosmosdb_container_name" {
  description = "The name of the Cosmos DB container."
  value       = azurerm_cosmosdb_sql_container.container.name
}
