from pathlib import Path

from PyQt6.QtWidgets import QFileDialog


def open_file(
    parent,
    dialog_title,
    dialog_location=Path("~").expanduser().as_posix(),
    file_filter=None,
):
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
    dialog_location=Path("~").expanduser().as_posix(),
    file_filter=None,
):
    return QFileDialog.getSaveFileName(
        parent,
        caption=dialog_title,
        directory=dialog_location,
        filter=file_filter,
        options=QFileDialog.DontUseNativeDialog,
    )
