resource "azurerm_app_configuration_key" "this" {
  for_each               = var.keys_map
  configuration_store_id = var.app_configuration_id  # This refers to the Azure App Configuration instance
  key                    = each.key                    # This is the key in App Configuration, e.g., "a:b:c"
  value                  = each.value                  # This is the value, e.g., the Key Vault secret URI
  content_type           = "application/vnd.microsoft.appconfig.keyvaultref+json;charset=utf-8"
}