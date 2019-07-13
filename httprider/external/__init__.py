from .requester import Requester

requester = Requester()


def open_form_file(file_location):
    return open(file_location, 'rb')
