import pandas as pd
import numpy as np  
from filelock import FileLock
import os


class CsvManager():
    def __init__(self, file_path):
        self.file_path = file_path
        self.lock_path = self.file_path + ".lock"

    def load_csv(self):
        csv_header = pd.read_csv(self.file_path, nrows=0)
        dates = [col for col in ["Date", "Created_At", "Last_Modified"] if col in csv_header.columns]
        return pd.read_csv(self.file_path, index_col="Id", parse_dates=dates)
        

    def save_csv(self, data_frame):
        data_frame.to_csv(self.file_path, index=True)

    def lock(self, timeout=10):
        return FileLock(self.lock_path, timeout=timeout)

    def generate_id(self, data_frame):
        id_max = data_frame.index.max()
        return  id_max + 1 if not np.isnan(id_max) else 1

