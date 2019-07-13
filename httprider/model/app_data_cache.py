import logging
from typing import List

from ..model.app_data import ApiCall, AppDataWriter, AppDataReader, AppState
from ..core.constants import DEFAULT_TAG


def _build_filter_query(query=None, tag=None):
    selected_tag = tag if tag != DEFAULT_TAG else None
    if selected_tag and query:
        return lambda api_call: query.lower() in api_call.title.lower() \
                                and selected_tag in api_call.tags

    if selected_tag:
        return lambda api_call: selected_tag in api_call.tags

    if query:
        return lambda api_call: query.lower() in api_call.title.lower()

    return lambda api_call: api_call


class AppDataCache:
    api_call_list: List[ApiCall] = []
    app_state: AppState = None
    search_query = None

    def __init__(self, data_reader: AppDataReader, data_writer: AppDataWriter):
        self.app_data_reader = data_reader
        self.app_data_writer = data_writer
        self.app_data_writer.signals.api_call_added.connect(self.on_api_call_added)
        self.app_data_writer.signals.api_call_removed.connect(self.on_api_call_removed)
        self.app_data_writer.signals.multiple_api_calls_added.connect(self.on_multiple_api_calls_added)
        self.app_data_writer.signals.api_call_tag_added.connect(lambda c: self.refresh_cache_item(c.id))
        self.app_data_writer.signals.api_call_tag_removed.connect(lambda c: self.refresh_cache_item(c.id))
        self.app_data_writer.signals.api_call_updated.connect(self.refresh_cache_item)
        self.app_data_writer.signals.app_state_updated.connect(self.refresh_app_state)

    def load_cache(self):
        self.api_call_list = self.app_data_reader.get_all_api_calls()
        self.app_state = self.app_data_reader.get_app_state()

    def refresh_app_state(self):
        self.app_state = self.app_data_reader.get_app_state()

    def refresh_cache_item(self, api_call_id):
        refreshed_api_call = self.app_data_reader.get_api_call(api_call_id)
        for ac in self.api_call_list:
            if ac.id == api_call_id:
                self.api_call_list.remove(ac)
        self.api_call_list.append(refreshed_api_call)

    def on_api_call_added(self, doc_id, api_call: ApiCall):
        api_call.id = doc_id
        self.api_call_list.append(api_call)

    def on_api_call_removed(self, doc_ids):
        for api_call in self.api_call_list:
            if api_call.id in doc_ids:
                self.api_call_list.remove(api_call)

    def on_multiple_api_calls_added(self, doc_ids: List[str], api_calls: List[ApiCall]):
        assert len(doc_ids) == len(api_calls)
        for doc_id, api_call in zip(doc_ids, api_calls):
            api_call.id = doc_id
            self.api_call_list.append(api_call)

    def filter_api_calls(self, search_query=None, search_tag=None):
        logging.info(f"Filtering API Calls by Query {search_query} and Tag {search_tag}")
        api_calls_filter = _build_filter_query(query=search_query, tag=search_tag)
        return sorted(
            filter(api_calls_filter, self.api_call_list),
            key=lambda a: a.sequence_number
        )

    def update_search_query(self, search_query):
        self.search_query = search_query

    def get_app_state(self):
        self.app_state.selected_search = self.search_query
        return self.app_state
