from pathlib import Path


def open_form_file(file_location):
    with Path(file_location).open("rb") as f:
        return f.read()
