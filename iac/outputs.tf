output "resource_group_id" {
  value = module.resource_group.resource_group_id
}

output "key_vault_id" {
  value = module.key_vault.key_vault_id
}

output "app_configuration_id" {
  value = module.app_configuration.app_configuration_id
}

output "storage_account_id" {
  value = module.blob_storage.storage_account_id
}

output "blob_container_id" {
  value = module.blob_storage.blob_container_id
}
