import enum


class ProjectCreationRoles(str, enum.Enum):
    editor = "roles/editor"
    viewer = "roles/viewer"
