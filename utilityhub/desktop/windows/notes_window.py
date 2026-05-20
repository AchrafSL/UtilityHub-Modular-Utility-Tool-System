from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QLineEdit, QTextEdit \
    , QPushButton, QHBoxLayout, QVBoxLayout, QComboBox, QListWidget \
        , QButtonGroup, QListWidgetItem

from PyQt5.QtCore import QThread, Qt, QSize

from modules.notes.notes_service import NotesService

class NotesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.notes_service = NotesService()
        self.tag_buttons = {}
        self.current_note_id = None # to store the id of the note being edited, None means new
        self.initUI()

    
    def initUI(self):
        self.master_layout = QHBoxLayout(self)

        # left frame -----------------------------------------
        self.left_frame = QFrame()
        self.left_frame_layout = QVBoxLayout(self.left_frame)
        self.left_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.left_frame_layout.setSpacing(0)


        # left_frame_header:
        self.left_frame_header = QFrame()
        self.left_frame_header.setLayout(QHBoxLayout())
        
        self.left_frame_title = QLabel("Notes")
        self.left_frame_note_counter = QLabel("0 NOTES")
        self.left_frame_add_notes_btn = QPushButton("+ New")
        self.left_frame_add_notes_btn.clicked.connect(self.clear_editor_for_new_note)

        self.left_frame_header.layout().addWidget(self.left_frame_title)
        self.left_frame_header.layout().addStretch() # send both sides in opposite directions
        self.left_frame_header.layout().addWidget(self.left_frame_note_counter)
        self.left_frame_header.layout().addWidget(self.left_frame_add_notes_btn)


        ## hr_line :
        self.left_frame_hr_line = QFrame()
        self.left_frame_hr_line.setFixedHeight(1)
        self.left_frame_hr_line.setStyleSheet("background-color: #3a3a36; border: none;")

        ## content container:
        self.left_frame_body = QFrame()
        self.left_frame_body.setLayout(QVBoxLayout())
        self.left_frame_body.setContentsMargins(16, 16, 16, 16)
        self.left_frame_body.layout().setSpacing(16)

        ### search
        self.left_frame_search = QLineEdit()
        self.left_frame_search.setPlaceholderText("Search notes ...")
        self.left_frame_search.textChanged.connect(self.on_search) 
        self.left_frame_body.layout().addWidget(self.left_frame_search)
        

        ### tags
        self.left_frame_tags_row = QFrame()
        self.left_frame_tag_row_layout = QHBoxLayout(self.left_frame_tags_row)
        self.left_frame_tag_row_layout.setContentsMargins(0, 0, 0, 0)
        self.left_frame_tag_row_layout.setSpacing(8)


        ### add tags:
        self.tag_button_group = QButtonGroup(self)
        self.tag_button_group.setExclusive(True)   # Enforce radio-behavior
        """
        add tags to same button grp
        add option exlusive to simulate radio behavior
        set chackable to true
        and for each btn click load the content based on the tag
        (search by tag)
        """

        categories = ["All", "General", "Work", "Dev", "Reading", "Personal"]
        for cat in categories:
            btn = QPushButton(cat)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setObjectName("tag_btn")       
            btn.setCheckable(True)      
            # when checkable is set: clicked auto send True/False state
            # _ here to absorbe that state
            btn.clicked.connect(lambda _,c=cat:self.load_notes(c))

            self.tag_button_group.addButton(btn) # link button to the group!
            


            self.tag_buttons[cat] = btn
            self.left_frame_tag_row_layout.addWidget(btn)

        self.left_frame_tag_row_layout.addStretch()
        self.tag_buttons["All"].setChecked(True) # All is default



        
        self.left_frame_body.layout().addWidget(self.left_frame_tags_row)

        ### notes container 
        self.left_frame_notes = QFrame()
        self.left_frame_notes_layout = QVBoxLayout(self.left_frame_notes)
        self.left_frame_notes_layout.setContentsMargins(0, 0, 0, 0)
        self.left_frame_notes_layout.setSpacing(8)

        ## add notes
        self.notes_list = QListWidget()
        self.notes_list.setSpacing(8) 
        self.notes_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.notes_list.itemClicked.connect(self.display_note)
        self.notes_list.setFixedHeight(245)
        

        self.left_frame_notes_layout.addWidget(self.notes_list)





        self.errorLabel = QLabel("No notes found.")
        self.errorLabel.setStyleSheet("color: #8b949e; font-size: 20px; padding: 16px;")
        self.errorLabel.hide()
        self.left_frame_notes.layout().addWidget(self.errorLabel)


        self.left_frame_body.layout().addWidget(self.left_frame_notes)



        ## add header and body to the left_frame
        self.left_frame_layout.addWidget(self.left_frame_header)
        self.left_frame_layout.addWidget(self.left_frame_hr_line)
        self.left_frame_layout.addWidget(self.left_frame_body)


        ## add the whole left frame to master layout:
        self.master_layout.addWidget(self.left_frame, 1, alignment=Qt.AlignmentFlag.AlignTop)



        # right frame -----------------------------------------------------------
        self.right_frame = QFrame()
        self.right_frame_layout = QVBoxLayout(self.right_frame)
        self.right_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.right_frame_layout.setSpacing(0)

        self.right_frame_header = QFrame()
        self.right_frame_header.setLayout(QHBoxLayout())


        self.right_frame_title = QLabel("New Note")
        self.right_frame_delete_notes_btn = QPushButton("Delete")
        self.right_frame_delete_notes_btn.clicked.connect(self.delete_current_note)
        self.right_frame_delete_notes_btn.hide()

        self.right_frame_header.layout().addWidget(self.right_frame_title)
        self.right_frame_header.layout().addStretch()
        self.right_frame_header.layout().addWidget(self.right_frame_delete_notes_btn)


        ## hr_line :
        self.right_frame_hr_line = QFrame()
        self.right_frame_hr_line.setFixedHeight(1)
        self.right_frame_hr_line.setStyleSheet("background-color: #3a3a36; border: none;")

        ## content container:
        self.right_frame_body = QFrame()
        self.right_frame_body.setLayout(QVBoxLayout())
        self.right_frame_body.setContentsMargins(16, 16, 16, 16)
        self.right_frame_body.layout().setSpacing(16)


        ### content:
        self.note_title_label = QLabel("TITLE")
        self.note_title_linedit = QLineEdit()
        self.note_title_linedit.setPlaceholderText("Note title...") 
        

        self.note_tag_label = QLabel("TAG")
        self.note_tag_dropdown = QComboBox()
        self.note_tag_dropdown.addItems(["General", "Work", "Dev", "Reading", "Personal"])

        self.note_content_label = QLabel("CONTENT")
        self.note_content_textedit = QTextEdit()
        self.note_content_textedit.setPlaceholderText("Write your note here...")
        self.note_content_textedit.textChanged.connect(self.update_char_count)


        self.status_row = QFrame()
        self.status_row_layout = QHBoxLayout(self.status_row)

        self.created_at_label = QLabel("-")
        self.last_modified_label = QLabel("-")
        self.chars_label = QLabel("0 chars")

        self.status_row_layout.addWidget(self.created_at_label)
        self.status_row_layout.addStretch() # pushes last_modifed to center
        self.status_row_layout.addWidget(self.last_modified_label)
        self.status_row_layout.addStretch() # push chars to far right
        self.status_row_layout.addWidget(self.chars_label)


        self.save_note = QPushButton("Save note")
        self.save_note.clicked.connect(self.save_current_note)

        




        self.right_frame_body.layout().addWidget(self.note_title_label)
        self.right_frame_body.layout().addWidget(self.note_title_linedit)

        self.right_frame_body.layout().addWidget(self.note_tag_label)
        self.right_frame_body.layout().addWidget(self.note_tag_dropdown)

        self.right_frame_body.layout().addWidget(self.note_content_label)
        self.right_frame_body.layout().addWidget(self.note_content_textedit)

        self.right_frame_body.layout().addWidget(self.status_row)

        self.right_frame_body.layout().addWidget(self.save_note)

        ## add header line and body to the left_frame
        self.right_frame_layout.addWidget(self.right_frame_header)
        self.right_frame_layout.addWidget(self.right_frame_hr_line)
        self.right_frame_layout.addWidget(self.right_frame_body)


        ## add the whole right frame to master layout:
        self.master_layout.addWidget(self.right_frame, 1)



        # styling css ------------------------------------------------
        self.left_frame.setObjectName("card")
        self.right_frame.setObjectName("card")

        self.left_frame_header.setObjectName("card_title")
        self.right_frame_header.setObjectName("card_title")

        self.left_frame_add_notes_btn.setObjectName("success_btn")
        self.save_note.setObjectName("convert_btn")
        self.right_frame_delete_notes_btn.setObjectName("danger_note")

        self.notes_list.setObjectName("notes_list")


        self.left_frame_add_notes_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.right_frame_delete_notes_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_note.setCursor(Qt.CursorShape.PointingHandCursor)
        self.note_tag_dropdown.setCursor(Qt.CursorShape.PointingHandCursor)



        ## initial load:
        self.load_notes("All")




    def load_notes(self, tag):
        self.notes_list.clear()

        notes = self.notes_service.search_by_tag(tag)

        if notes is not None and not notes.empty:
            self.errorLabel.hide()
            self.notes_list.show()

            # update note counter:
            count = len(notes)
            count = f"{len(notes)} NOTE" if count == 1 else f"{len(notes)} NOTES"
            self.left_frame_note_counter.setText(f"{count}")

            for id, note in notes.iterrows():
                content = str(note.get("Content",''))

                if content.lower() == "nan":
                    content = ""
                    
                snippet = content.strip().split('\n')[0]
                if snippet:
                    if len(snippet) > 59: # 59 is what lineedit max width chat in this case
                        snippet = snippet[:60] + "..."
                else:
                    snippet = "Empty Note..."

                idNote = id

                self.add_note_item(note['Title'], note['Last_Modified'].strftime("%Y-%m-%d"), snippet, note["Tag"], idNote)



        else:
            self.notes_list.hide()
            self.errorLabel.show()
            self.left_frame_note_counter.setText(f"{0} NOTES")


        pass 



    def display_note(self, item):
        idNote = item.data(Qt.ItemDataRole.UserRole)
        self.current_note_id = idNote


        note = self.notes_service.get_note_by_id(idNote)

        # show delete btn
        self.right_frame_delete_notes_btn.show()



        title = note['Title']
        content = note['Content']
        tag = note["Tag"]
        created_at = note['Created_At'].strftime("%Y-%m-%d")
        last_modified = note['Last_Modified'].strftime("%Y-%m-%d")
        chars = len(content)

        self.right_frame_title.setText(f"Editing: {title}")
        self.note_title_linedit.setText(title)
        self.note_tag_dropdown.setCurrentText(tag)
        self.note_content_textedit.setText(content)
        self.created_at_label.setText(created_at)
        self.last_modified_label.setText(last_modified)
        self.chars_label.setText(f"{chars} chars")
        




    def add_note_item(self, title, date_str, snippet ,tag, idNote):
        item = QListWidgetItem(self.notes_list)

        item.setData(Qt.ItemDataRole.UserRole, idNote)

        tag_colors = {
            "General": ("#39c5cf", "#10363a"),  # txt color, bg color
            "Work":    ("#f2cc60", "#4d3c11"),  
            "Dev":     ("#5DCAA5", "#04342C"),  
            "Reading": ("#e37b2d", "#4a2511"),  
            "Personal":("#52a8ff", "#042C53")   
        }

        text_color, bg_color = tag_colors.get(tag, ("#c9d1d9", "#21262d"))



        """
        i didn't knew this info before, i was using a Qlabel hidden,
        but QListWidgetItem comes with a secret storage u can save data in it
        using:
        item.setData and item.data

        """
        
        custom_widget = QWidget()
        custom_widget.setCursor(Qt.CursorShape.PointingHandCursor) 

        layout = QVBoxLayout(custom_widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-weight: bold; font-size: 20px; color: #c9d1d9;")
        
        lbl_snippet = QLabel(snippet)
        lbl_snippet.setStyleSheet("color: #8b949e; font-size: 18px;")
        lbl_snippet.setWordWrap(True)
        lbl_snippet.setMaximumHeight(24) 

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        
        lbl_date = QLabel(date_str)
        lbl_date.setStyleSheet("color: #8b949e; font-size: 16px;")
        
        lbl_tag = QLabel(tag)
        lbl_tag.setStyleSheet(f"""
            color: {text_color}; 
            background-color: {bg_color};
            border-radius: 10px;
            padding: 4px 12px;
            font-size: 16px;
            font-weight: bold;
        """)       

        row.addWidget(lbl_date)
        row.addStretch()      # Pushes tag to the far right
        row.addWidget(lbl_tag)
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_snippet)
        layout.addLayout(row)
        
        item.setSizeHint(custom_widget.sizeHint())
        self.notes_list.setItemWidget(item, custom_widget)



    def save_current_note(self):
        title = self.note_title_linedit.text().strip()
        tag = self.note_tag_dropdown.currentText().strip()
        content = self.note_content_textedit.toPlainText().strip()

        if not title and not content:
            return  # if empty dont save!

        if not title: title = "Untitled Note" # default title

        id = self.notes_service.save_note(title, content, tag, self.current_note_id)

        # if new update the edited current id:
        self.current_note_id = id

        # load the side-bar 
        self.tag_buttons["All"].setChecked(True)
        self.load_notes("All")
        

        
    def clear_editor_for_new_note(self):
        self.current_note_id = None
        self.note_title_linedit.clear()
        self.note_content_textedit.clear()
        self.right_frame_title.setText("New Note")
        self.chars_label.setText("0 chars")

        self.created_at_label.setText("-")
        self.last_modified_label.setText("-")
        self.note_tag_dropdown.setCurrentIndex(0)

        self.right_frame_delete_notes_btn.hide() 



    def delete_current_note(self):
        if self.current_note_id:

            self.notes_service.delete_note(self.current_note_id)

            self.clear_editor_for_new_note() 

            active_tag = self.tag_button_group.checkedButton().text()
            self.load_notes(active_tag) # Refresh sidebar

    


    def update_char_count(self):
        content = self.note_content_textedit.toPlainText()

        self.chars_label.setText(f"{len(content)} chars")



    def on_search(self, query):
        self.notes_list.clear()

        if not query:
            active_tag = self.tag_button_group.checkedButton().text()
            self.load_notes(active_tag)
            return

        notes = self.notes_service.search_notes(query)

        if notes is not None and not notes.empty:
            self.errorLabel.hide()
            self.notes_list.show()

            # update note counter:
            count = len(notes)
            self.left_frame_note_counter.setText(f"{count} Notes")

            for id, note in notes.iterrows():
                content = str(note.get("Content",''))
                if content.lower() == "nan": content = ""
                    
                snippet = content.strip().split('\n')[0]
                if snippet:
                    if len(snippet) > 59:
                        snippet = snippet[:60] + "..."
                else:
                    snippet = "Empty Note..."

                idNote = id
                self.add_note_item(note['Title'], note['Last_Modified'].strftime("%Y-%m-%d"), snippet, note["Tag"], idNote)

        else:
            self.notes_list.hide()
            self.errorLabel.show()
            self.left_frame_note_counter.setText("0 Notes")
        
        



