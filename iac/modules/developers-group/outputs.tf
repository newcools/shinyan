output "developers_group_id" {
  description = "The object ID of the Developers group."
  value       = azuread_group.developers_group.object_id
}

output "role_assignment_id" {
  description = "The ID of the role assignment."
  value       = azurerm_role_assignment.developers_role_assignment.id
}

output "developers_group_members" {
  description = "The list of members added to the Developers group."
  value       = [for member in azuread_group_member.developers_group_members : member.id]
}