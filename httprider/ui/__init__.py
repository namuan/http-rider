from pathlib import Path

from PyQt6.QtWidgets import QFileDialog


def open_file(
    parent,
    dialog_title,
    dialog_location=None,
    file_filter=None,
):
    if dialog_location is None:
        dialog_location = Path("~").expanduser().as_posix()
    return QFileDialog.getOpenFileName(
        parent,
        caption=dialog_title,
        directory=dialog_location,
        filter=file_filter,
        options=QFileDialog.DontUseNativeDialog,
    )


def save_file(
    parent,
    dialog_title,
    dialog_location=None,
    file_filter=None,
):
    if dialog_location is None:
        dialog_location = Path("~").expanduser().as_posix()
    return QFileDialog.getSaveFileName(
        parent,
        caption=dialog_title,
        directory=dialog_location,
        filter=file_filter,
        options=QFileDialog.DontUseNativeDialog,
    )
