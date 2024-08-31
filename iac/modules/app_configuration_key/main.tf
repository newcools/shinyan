resource "azurerm_app_configuration_key" "this" {
  name                 = var.key_name
  app_configuration_id = var.app_configuration_id
  key                  = var.key
  value                = var.value
  type                 = "KeyVaultReference"
  content_type         = "application/vnd.microsoft.appconfig.keyvaultref+json;charset=utf-8"
}