provider "azurerm" {
  features {}
}

# Create the Azure AD Group
resource "azuread_group" "developers_group" {
  display_name     = var.group_name
  security_enabled = true
}

# Assign a role to the group in the Resource Group
resource "azurerm_role_assignment" "developers_role_assignment" {
  principal_id        = azuread_group.developers_group.object_id
  role_definition_name = var.role_name  # Example: Contributor, Reader
  scope               = var.resource_group_id
}

# Add existing users to the group
resource "azuread_group_member" "developers_group_members" {
  for_each        = var.developer_upn_list
  group_object_id = azuread_group.developers_group.object_id
  member_object_id = lookup(each.value, "object_id", null)
}
