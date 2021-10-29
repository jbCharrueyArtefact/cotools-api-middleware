import json


class Secret:
    # to be changed when vault available
    def __init__(self, path_to_file):
        with open(path_to_file) as file:
            self.secrets = json.load(file)

    def get_secret(self, name):
        return self.secrets[name]
