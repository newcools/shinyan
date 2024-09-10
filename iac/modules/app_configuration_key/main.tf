data "azurerm_client_config" "current" {}

resource "azurerm_role_assignment" "appconfig_kv_reader" {
  principal_id         = var.app_configuration_identity
  role_definition_name = "Key Vault Secrets User"
  scope                = var.key_vault_id
}

resource "azurerm_key_vault_access_policy" "appconfig_keyvault_access" {
  key_vault_id = var.key_vault_id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = var.app_configuration_identity

  secret_permissions = [
    "Get",
    "List",
  ]
}

resource "azurerm_app_configuration_key" "this" {
  for_each               = var.keys_map
  configuration_store_id = var.app_configuration_id
  key                    = each.key
  type                   = "vault"
  vault_key_reference    = each.value
}