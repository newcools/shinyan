resource "azurerm_app_configuration_key" "this" {
  for_each             = var.keys_map
  name                 = each.key
  app_configuration_id = var.app_configuration_id
  key                  = each.key
  value                = each.value
  type                 = "KeyVaultReference"
  content_type         = "application/vnd.microsoft.appconfig.keyvaultref+json;charset=utf-8"
}
