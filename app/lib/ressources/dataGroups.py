from typing import List
from app.clients.bigqueryClient import BigQueryWrapper
from app.clients.groupClient import GroupClient
from app.config import GESTIONNAIRE_DATA
from datetime import datetime

from app.lib.utils.secret import (
    get_sa_info,
    get_sa_info_from_shared_data_vault,
)


class DataGroupsClient:
    def __init__(self):
        self.__db_client = BigQueryWrapper(get_sa_info("bq_shared_data"))
        self.__group_client = GroupClient(
            get_sa_info("group_creation"),
            get_sa_info_from_shared_data_vault("google_groups_assets"),
        )

    def _insert_group(
        self,
        name: str,
        description: str,
        entities: list[int],
        is_bank: bool,
        project: str,
        admin: str,
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

        data = [{"group_name": name, "admin": admin}]
        self.__db_client.insert_stream_data(GESTIONNAIRE_DATA, data)

    def _create_group(self, description, name):
        self.__group_client.create_group(name, description, name)

    def create_data_group(
        self,
        name: str,
        description: str,
        id_entities: list[str],
        is_bank: bool,
        project: str,
        admin: str,
    ):

        final_name = f"gcp-ofr-datagrp-{name}"

        self._insert_group(
            final_name, description, id_entities, is_bank, project, admin
        )
        self._create_group(description, final_name)
