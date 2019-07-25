import dataset


class Storage:
    def __init__(self, db_location):
        self.db = dataset.connect(f"sqlite:///{db_location}")
