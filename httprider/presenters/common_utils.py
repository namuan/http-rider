"""Common utility functions for presenters module."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView, QTreeWidgetItem

from httprider.core.constants import REPLACEMENTS
from httprider.model.app_data import ApiTestCase


def apply_replacements(replacements, input_str):
    """Apply replacements to input string."""
    for old, new in replacements:
        input_str = input_str.replace(old, new)
    return input_str


def assertion_variable_name(api_call_title, assertion_source, input_str):
    """Generate a variable name for assertions."""
    norm_title = apply_replacements(REPLACEMENTS, api_call_title.lower().strip())
    norm_input = apply_replacements(REPLACEMENTS, input_str.lower())

    if norm_input:
        return f"{ApiTestCase.DEFAULT_VAR_PREFIX}_{norm_title}_{assertion_source}_{norm_input}"
    else:
        return f"{ApiTestCase.DEFAULT_VAR_PREFIX}_{norm_title}_{assertion_source}"


def populate_tree_with_json(json_data, json_model, tree_view):
    """Populate a tree view with JSON data."""
    json_model.setup_model(json_data)
    tree_view.setModel(json_model)
    tree_view.expandAll()
    tree_view.header().setDefaultAlignment(Qt.AlignmentFlag.AlignHCenter)
    tree_view.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    tree_view.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)


def populate_tree_with_kv_dict(kv_dict, tree_widget):
    """Populate a tree widget with key-value dictionary."""
    tree_widget.clear()
    for hn, hv in kv_dict:
        item = QTreeWidgetItem([hn, hv])
        tree_widget.addTopLevelItem(item)
