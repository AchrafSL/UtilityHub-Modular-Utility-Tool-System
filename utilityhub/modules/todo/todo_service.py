from core.csv_manager import CsvManager
from core.history_manager import HistoryManager
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TODOPATH = os.path.join(BASE_DIR, "data", "todos.csv")

class TodoService:
    def __init__(self):
        self.csvmanager = CsvManager(TODOPATH)
        self.history_manager = HistoryManager("todo")

    
    def add_note(self, task):
        with self.csvmanager.lock():
            df = self.csvmanager.load_csv()
            record_id = self.csvmanager.generate_id(df)
            df.loc[record_id] = [task, "Pending", datetime.now()] # iloc doesn't allow creation
            self.csvmanager.save_csv(df)

            # save history:
            self.history_manager.add_record(f"Create Task", f"Created Task #{record_id}")
            return record_id


    def delete_task(self, id):
        with self.csvmanager.lock():
            df = self.csvmanager.load_csv()
            if (id in df.index) :
                df.drop(id, inplace = True, errors="ignore")
                self.csvmanager.save_csv(df)

                # save history:
                self.history_manager.add_record("Delete Task", f"Deleted Task #{id}")

                return True
            else:
                return False



    
    def change_status(self, id, new_status):
        with self.csvmanager.lock():
            df = self.csvmanager.load_csv()
            if (id in df.index):
                df.loc[id,"Status"] = new_status
                self.csvmanager.save_csv(df)

                self.history_manager.add_record("Modify Task", f"Changed status on Task #{id}")

                return True
            else:
                return False

            

    def change_task(self, id, new_task):
        with self.csvmanager.lock():
            df = self.csvmanager.load_csv()
            if (id in df.index):
                df.loc[id, "Task"] = new_task
                self.csvmanager.save_csv(df)

                self.history_manager.add_record("Modify Task", f"Changed task on Task #{id}")

                return True
            else:
                return False




    
    def get_tasks(self):
        df = self.csvmanager.load_csv()
        
        df_new = df.sort_values("Date", ascending=False)
        return df_new



    def search_tasks(self, keyword):
        df = self.csvmanager.load_csv()
        # na=False -> contains treats na as False
        cond = df['Task'].str.contains(keyword, case=False, na=False)

        search_df = df[ cond ].sort_values("Date", ascending=False)
        return search_df




    def search_by_status(self, status):
        df = self.csvmanager.load_csv()
        cond = df["Status"] == status # because UI support only 1 status

        search_df = df[ cond ].sort_values("Date", ascending=False)
        return search_df










