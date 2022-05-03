from app.config import DATA_GROUPS, GESTIONNAIRE_DATA
import datetime


def insert_group(
    self, name, description, entities, is_bank, project, admin, client
):
    data = [
        {
            "group_name": name,
            "description": description,
            "email": admin,
            "entities": entities,
            "is_banking": is_bank,
            "project": project,
            "creation_date": datetime.now().isoformat(),
        }
    ]

    self.insert_stream_data(DATA_GROUPS, data)
    data = [{"group_name": name, "admin": admin}]
    client.insert_stream_data(GESTIONNAIRE_DATA, data)
