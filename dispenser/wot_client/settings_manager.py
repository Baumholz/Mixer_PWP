import json

class SettingsManager:
    """Class for maintaining and updating the global settings.
    
    It simply wraps a python dictionary, which can be used to read any value/setting from. The
    dictionary can be saved to and loaded from a json file.
    Data/Settings can be accessed via the "data" property.
    """

    file_path = None
    data = {}

    def __init__(self, file_path) -> None:
        self.file_path = file_path
        file = open(file_path)
        self.data = json.load(file)
        file.close()
    
    def save(self) -> None:
        file = open(self.file_path, 'w')
        json.dump(self.data, file)
        file.close()


global_settings = SettingsManager('./wot_client/settings.json')
