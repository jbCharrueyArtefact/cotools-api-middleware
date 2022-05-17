from typing import List
from app.clients.bigqueryClient import BigQueryWrapper
from app.config import ENTITIES
from app.lib.utils.secret import get_sa_info


class EntitiesClient:
    def __init__(self):
        self.__db_client = BigQueryWrapper(get_sa_info("bq_shared_data"))

    def _is_existing_entity(self, entity_name):
        return entity_name in self._entities

    def existing_entity(self, entity_name: str):
        self._refresh()
        return self._is_existing_entity(entity_name)

    def existing_entities(self, entity_name_list: List[str]):
        self._refresh()
        for entity in entity_name_list:
            if self._is_existing_entity(entity):
                return False
        return True

    def _get_id_entity(self, entity_name):
        if self._is_existing_entity(entity_name):
            return self._entities[entity_name]

    def get_id_entity(self, entity_name):
        self._refresh()
        return self._get_id_entity()

    def get_list_id_entities(self, list_entity_name):
        self._refresh()
        return [self._get_id_entity(entity) for entity in list_entity_name]

    def fetch_entities(self):
        results = self.__db_client.query_data(f"select * from `{ENTITIES}`")
        return [{result.entity_name: result.ID} for result in results]

    def _refresh(self):
        self._entities = self.fetch_entities()
