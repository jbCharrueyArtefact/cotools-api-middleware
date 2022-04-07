import enum


class ProjectCreationRoles(str, enum.Enum):
    editor = "roles/editor"
    viewer = "roles/viewer"
    projectIamAdmin = "roles/resourcemanager.projectIamAdmin"
    serviceUsageAdmin = "roles/serviceusage.serviceUsageAdmin"
    serviceManagementConsumer = "roles/servicemanagement.serviceConsumer"
