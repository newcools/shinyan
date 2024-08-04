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
}

module "app_configuration" {
  source              = "./modules/app_configuration"
  resource_group_name = module.resource_group.resource_group_name
  location            = module.resource_group.location
}

module "blob_storage" {
  source              = "./modules/blob_storage"
  resource_group_name = module.resource_group.resource_group_name
  location            = module.resource_group.location
  storage_account_name = var.storage_account_name
  container_name      = "shinyan-files"
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