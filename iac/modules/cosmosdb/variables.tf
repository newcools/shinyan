variable "cosmosdb_account_name" {
  description = "The name of the Cosmos DB account."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group where the Cosmos DB account will be created."
  type        = string
}

variable "location" {
  description = "The Azure region where the Cosmos DB will be provisioned."
  type        = string
  default     = "Australia East"
}

variable "database_name" {
  description = "The name of the Cosmos DB database."
  type        = string
}

variable "container_name" {
  description = "The name of the Cosmos DB container."
  type        = string
}

variable "partition_key_path" {
  description = "The partition key path for the Cosmos DB container."
  type        = string
}

variable "principal_id" {
  description = "The ID of the Azure AD group or user to which Cosmos DB permissions will be assigned."
  type        = string
}
