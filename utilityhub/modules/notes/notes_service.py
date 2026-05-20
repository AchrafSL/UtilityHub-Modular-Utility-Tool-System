from core.csv_manager import CsvManager
from core.history_manager import HistoryManager
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOTESPATH = os.path.join(BASE_DIR, "data", "notes.csv")

class NotesService:
    def __init__(self):
        self.csvmanager = CsvManager(NOTESPATH)
        self.history_manager = HistoryManager("notes")

    
    def save_note(self, title, content, Tag="", id = None):
        with self.csvmanager.lock():
            df = self.csvmanager.load_csv()
            if id is None:
                record_id = self.csvmanager.generate_id(df)
                created_at = datetime.now()
            else:
                record_id = id
                created_at = df.loc[id]['Created_At'] 


            df.loc[record_id] = [title, content, created_at, datetime.now(), Tag] # iloc doesn't allow creation
            self.csvmanager.save_csv(df)
            

            # save history:
            self.history_manager.add_record(f"Create/Edit Note {title}", f"Saved Note #{record_id}")
            return record_id


    def delete_note(self, id):
        with self.csvmanager.lock():
            df = self.csvmanager.load_csv()
            if (id in df.index) :
                df.drop(id, inplace = True, errors="ignore")
                self.csvmanager.save_csv(df)

                # save history:
                self.history_manager.add_record("Delete Note", f"Deleted Note #{id}")

                return True
            else:
                return False



    
    def change_Tag(self, id, new_tag):
        with self.csvmanager.lock():
            df = self.csvmanager.load_csv()
            if (id in df.index):
                df.loc[id, ["Last_Modified", "Tag"]] = [datetime.now(), new_tag]  
                self.csvmanager.save_csv(df)

                self.history_manager.add_record("Modify Note", f"Changed Tag on Note #{id}")

                return True
            else:
                return False

    def change_Title(self, id, new_title):
        with self.csvmanager.lock():
            df = self.csvmanager.load_csv()
            if (id in df.index):
                df.loc[id, ["Last_Modified", "Title"]] = [datetime.now(), new_title]  
                self.csvmanager.save_csv(df)

                self.history_manager.add_record("Modify Note", f"Changed title on Note #{id}")

                return True
            else:
                return False

    def change_Content(self, id, new_content):
        with self.csvmanager.lock():
            df = self.csvmanager.load_csv()
            if (id in df.index):
                df.loc[id, ["Last_Modified", "Content"]] = [datetime.now(), new_content]  
                self.csvmanager.save_csv(df)

                self.history_manager.add_record("Modify Note", f"Changed Content on Note #{id}")
                return True
            else:
                return False




    def list_notes(self):
        return self.csvmanager.load_csv()


    def get_note_by_id(self, id):
        df = self.csvmanager.load_csv()
        return df.loc[id].to_dict()


    def search_notes(self, keyword):
        df = self.csvmanager.load_csv()
        # na=False -> contains treats na as False
        cond = df['Title'].str.contains(keyword, case=False, na=False) | df["Content"].str.contains(keyword, case=False, na=False)
        search_df = df[ cond ]
        return search_df



    def search_by_tag(self, tag_key):
        df = self.csvmanager.load_csv()
        df = df.sort_values(by="Last_Modified", ascending=False)


        if tag_key == "All":
            return df

        cond = df["Tag"] == tag_key # because UI support only 1 tag
        return df[ cond ]

