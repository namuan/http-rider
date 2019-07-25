import logging
from typing import List

from httprider.core import gen_uuid
from httprider.core.core_settings import app_settings
from httprider.model import ApiCall


class ApiCallInteractor:
    def add_api_call(self, api_call: ApiCall) -> str:
        api_call.id = gen_uuid()
        app_settings.app_data_writer.update_api_call_in_db(api_call)
        app_settings.app_data_writer.signals.api_call_added.emit(api_call.id, api_call)

        logging.info(f"DB {api_call.id} - Successfully added new API {api_call}")
        return api_call.id

    def add_multiple_api_calls(self, api_calls: List[ApiCall]) -> List[str]:
        if not api_calls:
            return []

        doc_ids = [
            self.add_api_call(api_call)
            for api_call in api_calls
        ]

        app_settings.app_data_writer.signals.multiple_api_calls_added.emit(doc_ids, api_calls)

        return doc_ids

    def remove_api_call(self, api_call_ids):
        logging.info(f"DB: Removing API Call with Ids: {api_call_ids}")
        app_settings.app_data_writer.delete_api_call_from_db(api_call_ids)
        app_settings.app_data_writer.signals.api_call_removed.emit(api_call_ids)

    def update_api_call(self, api_call_id, api_call):
        logging.info(f"DB API : {api_call_id} - Updating API Call {api_call}")
        api_call.id = api_call_id
        app_settings.app_data_writer.update_api_call_in_db(api_call)
        app_settings.app_data_writer.signals.api_call_updated.emit(api_call.id, api_call)

    def update_selected_api_call(self, doc_id):
        api_call = app_settings.app_data_cache.get_api_call(doc_id)
        logging.debug(f"update_selected_api_call: {doc_id} = {api_call}")
        app_settings.app_data_reader.signals.api_call_change_selection.emit(api_call)

    def add_tag_to_api_call(self, api_call: ApiCall, new_tag_name: str):
        logging.info(f"DB API : {api_call.id} - Adding tag {new_tag_name}")
        api_call.tags.append(new_tag_name)
        app_settings.app_data_writer.update_api_call_in_db(api_call)
        app_settings.app_data_writer.signals.api_call_tag_added.emit(api_call, new_tag_name)

    def remove_tag_from_api_call(self, api_call: ApiCall, tag_name: str):
        logging.info(f"DB API: {api_call.id} - Removing tag {tag_name}")
        api_call.tags.remove(tag_name)
        app_settings.app_data_writer.update_api_call_in_db(api_call)
        app_settings.app_data_writer.signals.api_call_tag_removed.emit(api_call, tag_name)

    def rename_tag_in_api_call(self, api_call: ApiCall, old_tag_name, new_tag_name):
        logging.info(f"DB API: {api_call.id} - Renaming tag {old_tag_name} to {new_tag_name}")
        api_call.tags.remove(old_tag_name)
        api_call.tags.append(new_tag_name)

        app_settings.app_data_writer.update_api_call_in_db(api_call)
        app_settings.app_data_writer.signals.api_call_tag_added.emit(api_call, new_tag_name)


api_call_interactor = ApiCallInteractor()
