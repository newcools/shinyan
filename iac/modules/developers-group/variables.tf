variable "group_name" {
  description = "The name of the Azure AD group to be created."
  type        = string
}

variable "resource_group_id" {
  description = "The ID of the resource group where the role will be assigned."
  type        = string
}

variable "role_name" {
  description = "The name of the role to assign to the group (e.g., Contributor, Reader)."
  type        = string
  default     = "Contributor"
}

variable "developer_upn_list" {
  description = "A map of user display names to their corresponding user object IDs."
  type        = map(object({
    object_id = string
  }))
}
