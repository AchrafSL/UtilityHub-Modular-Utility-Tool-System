import os
import json

# SETTINGS_PATH = r"utilityhub\data\settings.json" using this method 
# result problems in working directory search 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(BASE_DIR, "data", "settings.json")

class SettingsManager:
    def __init__(self):
        self.settings_path = SETTINGS_PATH

    
    def get_setting(self, category, key):
        with open(self.settings_path, "r") as file:
            data = json.load(file) # load for files, loads for string

        return data[category][key]
    

    def update_setting(self, category, key, value):
        with open(self.settings_path, "r") as file:
            data = json.load(file)

        data[category][key] = value

        with open(self.settings_path, "w") as file:
            json.dump(data, file, indent=2)


    def get_all_settings(self):
        with open(self.settings_path, "r") as file:
            return json.load(file)



