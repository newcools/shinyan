data "azurerm_client_config" "current" {}

resource "azurerm_app_configuration" "this" {
  name                = "${var.resource_group_name}-appconfig-free"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = var.sku
}

resource "azurerm_role_assignment" "app_configuration_role" {
  scope                = var.resource_group_id
  role_definition_name = "App Configuration Data Owner"
  principal_id         = data.azurerm_client_config.current.object_id
}