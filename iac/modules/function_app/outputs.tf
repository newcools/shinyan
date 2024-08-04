output "function_app_id" {
  value = azurerm_function_app.this.id
}

output "managed_identity_id" {
  value = azurerm_user_assigned_identity.this.id
}

output "app_service_plan_id" {
  value = azurerm_app_service_plan.this.id
}
