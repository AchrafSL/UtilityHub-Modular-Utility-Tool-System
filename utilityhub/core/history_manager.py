import pandas as pd
from core.csv_manager import CsvManager
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(BASE_DIR, "data", "history.csv")

class HistoryManager():
    def __init__(self, tool):
        self.file_path = HISTORY_PATH
        self.csv_manager = CsvManager(self.file_path)
        self.tool = tool
    
    def add_record(self, request, response):
        with self.csv_manager.lock():
            df = self.csv_manager.load_csv()

            # the final file is playing the role of the id
            cond = (df['Tool'] == self.tool) & (df['Response'] == response) 

            if any(cond):
                    df.loc[cond, 'Date'] = datetime.now()
                    df.loc[cond, 'Request'] = request
            else:
                record_id = self.csv_manager.generate_id(df)

                current_datetime = datetime.now()
                df.loc[record_id] = [self.tool, request, response, current_datetime]

            self.csv_manager.save_csv(df)


    def get_history(self):
        df = self.csv_manager.load_csv()
        return df[df['Tool'] == self.tool]



    def clear_history(self):
        with self.csv_manager.lock():
            df = self.csv_manager.load_csv()

            df_new = df[df['Tool'] != self.tool]
            self.csv_manager.save_csv(df_new)



    def delete_record(self, id):
        with self.csv_manager.lock():
            df = self.csv_manager.load_csv()

            df.drop(id, inplace=True, errors="ignore")
            self.csv_manager.save_csv(df)

