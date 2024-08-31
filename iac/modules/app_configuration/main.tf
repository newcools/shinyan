resource "azurerm_app_configuration" "this" {
  name                = "${var.resource_group_name}-appconfig-free"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = var.sku
}