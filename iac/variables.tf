variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "shinyan"
}

variable "location" {
  description = "Azure location where resources will be deployed"
  type        = string
  default     = "Australia East"
}

variable "storage_account_name" {
  description = "Name of the storage account"
  type        = string
  default     = "shinyastorage"
}

variable "openai_api_key" {
  description = "The value of the OpenAI API key."
  type        = string
  sensitive   = true
}

variable "cosmosdb_account_name" {
  description = "The name of the Cosmos DB account."
  type        = string
  default     = "shinyan-cosmosdb"  # Default Cosmos DB account name
}

variable "cosmosdb_database_name" {
  description = "The name of the Cosmos DB database."
  type        = string
  default     = "shinyan-database"  # Default database name
}

variable "cosmosdb_container_name" {
  description = "The name of the Cosmos DB container."
  type        = string
  default     = "cards"  # Default container name
}

variable "partition_key_path" {
  description = "The partition key path for the Cosmos DB container."
  type        = string
  default     = "/deck"
}

variable "developer_upn_list" {
  description = "A map of user display names to their corresponding user object IDs."
  type        = map(object({
    object_id = string
  }))
  default = {}
}