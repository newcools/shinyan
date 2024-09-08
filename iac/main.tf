module "resource_group" {
  source              = "./modules/resource_group"
  resource_group_name = var.resource_group_name
  location            = var.location
}

module "key_vault" {
  source              = "./modules/key_vault"
  resource_group_name = module.resource_group.resource_group_name
  location            = module.resource_group.location
  tenant_id           = data.azurerm_client_config.shinyan.tenant_id
  object_id           = data.azurerm_client_config.shinyan.object_id
  openai_api_key      = var.openai_api_key
}

module "app_configuration" {
  source              = "./modules/app_configuration"
  resource_group_name = module.resource_group.resource_group_name
  resource_group_id   = module.resource_group.resource_group_id
  location            = module.resource_group.location
}

module "app_configuration_key_vault" {
  source               = "./modules/app_configuration_key"
  app_configuration_id = module.app_configuration.app_configuration_id
  
  keys_map = {
    "openai__api_key" = module.key_vault.openai_api_key_uri
  }
}

module "blob_storage" {
  source              = "./modules/blob_storage"
  resource_group_name = module.resource_group.resource_group_name
  location            = module.resource_group.location
  storage_account_name = var.storage_account_name
  container_name      = "shinyan-files"
}

module "cosmosdb" {
  source              = "./modules/cosmosdb"
  cosmosdb_account_name = var.cosmosdb_account_name
  resource_group_name = module.resource_group.resource_group_name
  location            = var.location  # Default location: Australia East
  database_name       = var.cosmosdb_database_name
  container_name      = var.cosmosdb_container_name
  partition_key_path  = var.partition_key_path

  # Pass the principal ID of the Developers group to the Cosmos DB module for role assignment
  principal_id = module.developers_group.developers_group_id
}

# Call the Developers Group Module
module "developers_group" {
  source            = "./modules/developers-group"
  group_name        = "developers"
  resource_group_id = module.resource_group.resource_group_id
  role_name         = "Contributor"

  developer_upn_list = var.developer_upn_list  # Reads from tfvars
}



# module "function_app" {
#   source                     = "./modules/function_app"
#   resource_group_name        = module.resource_group.resource_group_name
#   location                   = module.resource_group.location
#   function_app_name          = var.function_app_name
#   storage_account_name       = module.blob_storage.storage_account_name
#   key_vault_id               = module.key_vault.key_vault_id
#   key_vault_name             = module.key_vault.key_vault_name
#   managed_identity_name      = var.managed_identity_name
#   app_service_plan_id        = module.app_service_plan.id
# }
# 
# variable "managed_identity_name" {
#   description = "Name of the User Assigned Managed Identity"
#   type        = string
#   default     = "shinya-identity"
# }