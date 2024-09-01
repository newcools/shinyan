resource "azurerm_app_configuration_key" "this" {
  for_each               = var.keys_map
  configuration_store_id = var.app_configuration_id
  key                    = each.key
  value                  = each.value
}