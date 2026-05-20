from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QListWidget \
, QListWidgetItem, QComboBox, QCheckBox, QWidget, QHBoxLayout, QVBoxLayout, QFrame \
, QTextEdit, QSizePolicy

from PyQt5.QtCore import Qt


from modules.todo.todo_service import TodoService

class TodoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.todo_service = TodoService()
        self.all_status_data = ["Done", "In-progress", "Pending"]
        self.initUI()


    def initUI(self):
        self.master_layout = QHBoxLayout()
        self.setLayout(self.master_layout)

        # left-card --------------------------------------
        self.left_card = QFrame()
        self.left_card.setLayout(QVBoxLayout())

        self.left_card_top = QFrame()
        self.left_card_top.setLayout(QVBoxLayout())

        self.left_card_bottom = QFrame()
        self.left_card_bottom.setLayout(QVBoxLayout())

  

        # left-card-top ----------------------------------
        self.add_task_label = QLabel("ADD TASK")
        self.add_task_description_label = QLabel("TASK DESCRIPTION")
        self.add_description_lineEdit = QLineEdit()
        self.add_description_lineEdit.setPlaceholderText("Describe the task")

        self.add_task_btn = QPushButton("Add task")
        self.add_task_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_task_btn.clicked.connect(self.addTask)

        self.hr_line1 = QFrame()
        self.hr_line1.setFixedHeight(1)
        self.hr_line1.setStyleSheet("background-color: #3a3a36; border: none;")


        self.left_card_top.layout().addWidget(self.add_task_label)
        self.left_card_top.layout().addWidget(self.hr_line1)
        self.left_card_top.layout().addWidget(self.add_task_description_label)
        self.left_card_top.layout().addWidget(self.add_description_lineEdit)
        self.left_card_top.layout().addWidget(self.add_task_btn)

        # left-card-bottom ----------------------------------
        self.filter_task_label = QLabel("FILTER")
        self.filter_keyword_label = QLabel("KEYWORD")
        self.filter_search_lineedit = QLineEdit()
        self.filter_search_lineedit.setPlaceholderText("Seach tasks...") 
        self.filter_search_lineedit.textChanged.connect(self.on_text_changed)

        self.filter_status_label = QLabel("STATUS")
        self.filter_dropdown = QComboBox()
        self.filter_dropdown.setCursor(Qt.CursorShape.PointingHandCursor)
        self.filter_dropdown.addItems(["All", "Pending", "In-progress", "Done"])
        self.filter_dropdown.currentIndexChanged.connect(self.on_search_index_change)
        
        self.filter_count_label = QLabel("0 tasks")

        self.hr_line2 = QFrame()
        self.hr_line2.setFixedHeight(1)
        self.hr_line2.setStyleSheet("background-color: #3a3a36; border: none;")


        self.left_card_bottom.layout().addWidget(self.filter_task_label)
        self.left_card_bottom.layout().addWidget(self.hr_line2)
        self.left_card_bottom.layout().addWidget(self.filter_search_lineedit)
        self.left_card_bottom.layout().addWidget(self.filter_status_label)
        self.left_card_bottom.layout().addWidget(self.filter_dropdown)
        self.left_card_bottom.layout().addWidget(self.filter_count_label)


        self.left_card.layout().addWidget(self.left_card_top)
        self.left_card.layout().addWidget(self.left_card_bottom)

        self.master_layout.addWidget(self.left_card, 1, alignment=Qt.AlignmentFlag.AlignTop)


        # right part:
        self.right_card = QFrame()
        self.right_card.setLayout(QVBoxLayout())

        ## active frame:
        self.active_frame = QFrame()
        self.active_frame.setLayout(QVBoxLayout())

        self.active_header = QFrame()
        self.active_header_layout = QHBoxLayout(self.active_header)
        self.active_header_layout.setContentsMargins(10, 5, 10, 5)

        self.active_label = QLabel("ACTIVE")
        self.active_count = QLabel("0")

        self.active_hr = QFrame()
        self.active_hr.setFixedHeight(1)
        self.active_hr.setStyleSheet("background-color: #3a3a36; border: none;")

        self.active_header_layout.addWidget(self.active_label)
        self.active_header_layout.addStretch()
        self.active_header_layout.addWidget(self.active_count)
        
        self.active_frame.layout().addWidget(self.active_header)
        self.active_frame.layout().addWidget(self.active_hr)

        ## active_list:
        self.active_list = QListWidget()
        self.active_list.setSpacing(10)

        self.active_frame.layout().addWidget(self.active_list)



        ## Done frame:
        self.done_frame = QFrame()
        self.done_frame.setLayout(QVBoxLayout())

        self.done_header = QFrame()
        self.done_header_layout = QHBoxLayout(self.done_header)
        self.done_header_layout.setContentsMargins(10, 5, 10, 5)

        self.done_label = QLabel("DONE")
        self.done_count = QLabel("0")

        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear.clicked.connect(self.clear_done_tasks)

        self.btn_clear.hide()

        self.done_hr = QFrame()
        self.done_hr.setFixedHeight(1)
        self.done_hr.setStyleSheet("background-color: #3a3a36; border: none;")

        self.done_header_layout.addWidget(self.done_label)
        self.done_header_layout.addStretch()
        self.done_header_layout.addWidget(self.done_count)
        self.done_header_layout.addWidget(self.btn_clear)
        
        self.done_frame.layout().addWidget(self.done_header)
        self.done_frame.layout().addWidget(self.done_hr)

        ## done_list:
        self.done_list = QListWidget()
        self.done_list.setSpacing(10)

        self.done_frame.layout().addWidget(self.done_list)

        self.right_card.layout().addWidget(self.active_frame, 1)
        self.right_card.layout().addWidget(self.done_frame, 1)
        self.right_card.layout().setSpacing(20)

        self.master_layout.addWidget(self.right_card, 1)


        # ------------------- Styling (CSS) ----------------------------------
        self.left_card_top.setObjectName("card")   
        self.left_card_bottom.setObjectName("card")   
        self.active_frame.setObjectName("card")
        self.done_frame.setObjectName("card")

        self.add_task_label.setObjectName("section_title")
        self.filter_task_label.setObjectName("section_title")
        self.active_label.setObjectName("section_title")
        self.done_label.setObjectName("section_title")

        self.active_count.setObjectName("count_badge")
        self.done_count.setObjectName("count_badge")

        self.filter_count_label.setObjectName("filter_count")
        self.add_task_btn.setObjectName("todo_add_btn")

        self.btn_clear.setObjectName("danger_btn")


        




        # initial load:
        self.load_tasks()




    def addTask(self):
        task_content = self.add_description_lineEdit.text()
        if task_content:
            idN = self.todo_service.add_note(task_content)
            self.addListItem(False, task_content, "Pending", idN)
            self.add_description_lineEdit.clear()


    def change_status(self, checked, item):
        id = item.data(Qt.ItemDataRole.UserRole)

        if checked:
            self.todo_service.change_status(id, "Done")

        else:
            self.todo_service.change_status(id,"Pending")

        self.load_tasks()



    def clear_tasks_visually(self):
        self.done_list.clear()
        self.active_list.clear()

    def load_tasks(self):
        self.clear_tasks_visually() # clear before loading

        tasks_df = self.todo_service.get_tasks()
        for id, task in tasks_df.iterrows():
            content = task["Task"]
            status = task["Status"]
            checked = True if status == "Done" else False

            self.addListItem(checked, content, status, id)


        self.update_counts()




            

        


    def addListItem(self, checked, task_content, status, idN):

        target_list = self.done_list if checked else self.active_list
        item =  QListWidgetItem(target_list)
        item.setData(Qt.ItemDataRole.UserRole, idN)

        row_widget = QFrame()
        row_widget.setLayout(QHBoxLayout())
        row_widget.setObjectName("card")
        row_widget.layout().setContentsMargins(15, 15, 15, 15)
        row_widget.layout().setSpacing(15)

        check_box = QCheckBox()
        check_box.setCursor(Qt.CursorShape.PointingHandCursor)
        check_box.setChecked(checked)
        check_box.toggled.connect(lambda checked, item = item: self.change_status(checked,item))


        task_content_label = QTextEdit(task_content)
        task_content_label.setObjectName("task_content")
        task_content_label.setReadOnly(True)
        task_content_label.document().setDocumentMargin(0) # remove internal margin of the QTextEdit
        task_content_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        task_content_label.setFixedHeight(80)




        task_dropdown = QComboBox()
        task_dropdown.setCursor(Qt.CursorShape.PointingHandCursor)
        
        task_dropdown.addItems(self.all_status_data)
        task_dropdown.setCurrentIndex(self.all_status_data.index(status))
        task_dropdown.setObjectName("task_status_dropdown")
        task_dropdown.setProperty("status", status)
        task_dropdown.currentIndexChanged.connect(lambda index, item=item: self.on_index_change(index, item))





        row_widget.layout().addWidget(check_box, 0, Qt.AlignmentFlag.AlignVCenter)
        row_widget.layout().addWidget(task_content_label, 1, Qt.AlignmentFlag.AlignVCenter)
        row_widget.layout().addWidget(task_dropdown, 0, Qt.AlignmentFlag.AlignVCenter)

            

        item.setSizeHint(row_widget.sizeHint())
        target_list.setItemWidget(item, row_widget)


    def on_index_change(self, index, item):
        id = item.data(Qt.ItemDataRole.UserRole)
        status = self.all_status_data[index]

        self.todo_service.change_status(id, status)

        self.load_tasks()


    def on_text_changed(self, keyword):
        searched_df = self.todo_service.search_tasks(keyword)

        self.clear_tasks_visually() # clear before loading

        for id, task in searched_df.iterrows():
            content = task["Task"]
            status = task["Status"]
            checked = True if status == "Done" else False

            self.addListItem(checked, content, status, id)

        self.update_counts()









    def on_search_index_change(self, index):
        if index == 0:
            self.load_tasks()
            return 
        else:
            status = self.filter_dropdown.itemText(index)
            searched_df = self.todo_service.search_by_status(status)


        self.clear_tasks_visually() # clear before loading

        for id, task in searched_df.iterrows():
            content = task["Task"]
            status = task["Status"]
            checked = True if status == "Done" else False

            self.addListItem(checked, content, status, id)

        self.update_counts()



    def update_counts(self):
        self.active_count.setText(str(self.active_list.count()))
        self.done_count.setText(str(self.done_list.count()))

        total = self.active_list.count() + self.done_list.count()
        self.filter_count_label.setText(f"{total} tasks")

        is_there_tasks = self.done_list.count() > 0
        self.btn_clear.setVisible(is_there_tasks)



    def clear_done_tasks(self):
        done_dfs = self.todo_service.search_by_status("Done")

        for idT, task in done_dfs.iterrows():
            self.todo_service.delete_task(idT)

        self.load_tasks()
