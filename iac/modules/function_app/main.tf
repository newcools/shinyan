resource "azurerm_user_assigned_identity" "this" {
  name                = var.managed_identity_name
  resource_group_name = var.resource_group_name
  location            = var.location
}

resource "azurerm_app_service_plan" "this" {
  name                = "${var.function_app_name}-plan"
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "FunctionApp"
  reserved            = true

  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

resource "azurerm_function_app" "this" {
  name                       = var.function_app_name
  location                   = var.location
  resource_group_name        = var.resource_group_name
  app_service_plan_id        = azurerm_app_service_plan.this.id
  storage_account_name       = var.storage_account_name
  storage_account_access_key = var.storage_account_access_key
  version                    = "~3"
  identity {
    type = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.this.id]
  }
  app_settings = {
    FUNCTIONS_EXTENSION_VERSION = "~3"
    WEBSITE_RUN_FROM_PACKAGE    = "1"
  }
  site_config {
    always_on = true
  }
}

resource "azurerm_key_vault_access_policy" "this" {
  key_vault_id = var.key_vault_id
  tenant_id    = var.tenant_id
  object_id    = azurerm_user_assigned_identity.this.principal_id

  secret_permissions = [
    "get",
    "list",
  ]

  depends_on = [azurerm_key_vault.this]
}
