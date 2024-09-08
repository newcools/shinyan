output "cosmosdb_account_id" {
  description = "The ID of the Cosmos DB account."
  value       = azurerm_cosmosdb_account.cosmosdb_serverless.id
}