resource "azurerm_app_configuration" "this" {
  name                = "${var.resource_group_name}-appconfig"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "free"
}