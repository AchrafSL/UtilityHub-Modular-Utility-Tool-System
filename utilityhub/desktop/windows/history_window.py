from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton\
    , QListWidget, QListWidgetItem, QWidget, QScrollArea


from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from core.history_manager import HistoryManager
from core.csv_manager import CsvManager
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HISTORY_PATH = os.path.join(BASE_DIR, "data", "history.csv")

class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.csv_manager = CsvManager(HISTORY_PATH)
        self.initUI()


    def initUI(self):
        self.master_layout = QVBoxLayout(self)


        self.history_frame = QFrame()
        self.history_frame.setLayout(QVBoxLayout())
        self.history_frame.setContentsMargins(0, 0, 0, 0)
        self.history_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.history_frame.setFixedHeight(590)

        self.history_frame.setStyleSheet("padding:0px;")

        self.header_row = QFrame()
        self.header_row.setLayout(QHBoxLayout())
        self.header_row.layout().setContentsMargins(0, 0, 0, 0)
        self.header_row.layout().setSpacing(0)
        self.header_row.setStyleSheet("padding: 10px 15px;")

        self.header_label = QLabel("ACTION HISTORY")
        self.clear_all = QPushButton("Clear all")
        self.clear_all.setStyleSheet("padding:5px;")
        self.clear_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_all.clicked.connect(self.on_clear_all)

        self.header_row.layout().addWidget(self.header_label)
        self.header_row.layout().addStretch()
        self.header_row.layout().addWidget(self.clear_all)


        # column names:
        self.column_row = QFrame()
        self.column_row.setLayout(QHBoxLayout())

        
    

        self.tool_label = QLabel("Tool")
        self.request_label = QLabel("Request")

        self.response_label = QLabel("Response")

        self.date_label = QLabel("DATETIME")
        self.clear_zone = QLabel("")

        self.column_row.layout().addWidget(self.tool_label)
        self.column_row.layout().addStretch()
        self.column_row.layout().addWidget(self.request_label)
        self.column_row.layout().addStretch()
        self.column_row.layout().addWidget(self.response_label)
        self.column_row.layout().addStretch()
        self.column_row.layout().addWidget(self.date_label)
        self.column_row.layout().addStretch()
        self.column_row.layout().addWidget(self.clear_zone)


        self.tool_label.setFixedWidth(120)
        self.request_label.setFixedWidth(300)
        self.response_label.setFixedWidth(300)
        self.date_label.setFixedWidth(400)


        # Remove default layout margins
        self.column_row.layout().setContentsMargins(0, 0, 0, 0)
        self.column_row.layout().setSpacing(0)
        self.column_row.setObjectName("column_row")
        self.column_row.setStyleSheet("""
            #column_row {
                background-color: #1E1E1C;
                border: 1px solid #3a3a36;
                margin-bottom: 0px;
                padding: 15px 30px;

            }
                                      """)

        self.area = QFrame()
        self.area.setLayout(QVBoxLayout())


        self.history_list = QListWidget()
        self.history_list.setObjectName("history_list")

        
        self.noItems_label = QLabel("""No history found.
Start by using one of the tools to generate activity.""")
        self.noItems_label.setStyleSheet("padding: 30px 30px;")
        self.noItems_label.hide()
        self.area.layout().addWidget(self.noItems_label)
        


        self.area.layout().addWidget(self.history_list)
        self.area.layout().setContentsMargins(0, 0, 0, 0)
        self.area.layout().setSpacing(0)



        self.history_frame.layout().addWidget(self.header_row)
        self.history_frame.layout().addWidget(self.column_row)
        self.history_frame.layout().addWidget(self.area)
        self.history_frame.layout().setSpacing(0)


        self.master_layout.addWidget(self.history_frame, alignment = Qt.AlignmentFlag.AlignTop)

        self.load_history_items()


        # -------------- Styling (css) -------------------------------
        self.history_frame.setObjectName("history_card")
        self.header_row.setObjectName("card_title")
        self.clear_all.setObjectName("danger_btn")












    def load_history_items(self):
        self.clear_all_history_UI()

        history_df = self.csv_manager.load_csv()

        if history_df is not None and not history_df.empty:
            self.noItems_label.hide()
            for idH, history in history_df.iterrows():

                tool = history['Tool']

                request = history['Request']                
                response =  history['Response']

                if tool == "converter":
                    request = os.path.basename(request)
                    response = os.path.basename(response)
                elif tool == "downloader":
                    response = os.path.basename(response) if response else "FAILED TO FETCH"
                # NOW truncate the text for display (after cleaning the paths)
                request = request if len(request) < 20 else request[:20] + "..."
                response = response if len(response) < 20 else response[:20] + "..."



                date = history['Date'].strftime("%Y-%m-%d %H:%M")

                self.add_list_item(idH, tool, request, response, date)

        else:
            self.noItems_label.show()






    def clear_all_history_UI(self):
        self.history_list.clear()



    def add_list_item(self, idItem, tool, request, response, date):
        item = QListWidgetItem(self.history_list)
        data = {"item_id":idItem,
                "tool":tool
                }
        item.setData(Qt.ItemDataRole.UserRole, data)

        custom_row = QWidget()
        custom_row.setLayout(QHBoxLayout())

        tool_label = QLabel(tool)
        request_label = QLabel(request)
        response_label = QLabel(response)
        date_label = QLabel(date)
        
        btn_clear = QPushButton("")
        btn_clear.setIcon(QIcon(r"utilityhub\assets\red_X_icon.png"))
        btn_clear.setIconSize(QSize(16, 16))
        btn_clear.setFixedSize(30, 30)
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setObjectName("history_del")
        btn_clear.setStyleSheet("""
            #history_del {
                background: transparent;
                border: none;
            }
            #history_del:hover {
                background-color: rgba(255, 82, 82, 0.1);
                border-radius: 15px;
            }
        """)
        btn_clear.clicked.connect(lambda _,item=item: self.on_clear_item(item))


        # styling for tool label:
        color_style = {
            "converter": ('#2186E1', '#042C53'), # font/border color , bg color
            "downloader":('#2FBEA5', '#04342C'),
            "notes":('#EF9F1A',"#412402"),
            "todo":("#F09584" ,"#501313")
        }

        item_coloring = color_style.get(tool, ("#3a3a36", "#272724"))
        
        tool_label.setStyleSheet(f"""
                background-color: {item_coloring[1]};
                border: 1px solid {item_coloring[0]};
                border-radius: 10px;
                padding: 1px 8px;
                color: {item_coloring[0]};
                qproperty-alignment: 'AlignCenter'; 
                font-size: 18px;
                font-weight: bold;
                min-width: 100px;
                max-height: 30px;     


        """)


        custom_row.layout().addWidget(tool_label)
        custom_row.layout().addStretch()
        custom_row.layout().addWidget(request_label)
        custom_row.layout().addStretch()
        custom_row.layout().addWidget(response_label)
        custom_row.layout().addStretch()
        custom_row.layout().addWidget(date_label)
        custom_row.layout().addStretch()
        custom_row.layout().addWidget(btn_clear)


        tool_label.setFixedWidth(120)
        request_label.setFixedWidth(300)
        response_label.setFixedWidth(300)
        date_label.setFixedWidth(400)
        btn_clear.setFixedWidth(30)

        # Match margins with the header row
        custom_row.setStyleSheet("padding: 5px 15px; border-radius: 0px;")

        item.setSizeHint(custom_row.sizeHint()) 
        self.history_list.setItemWidget(item, custom_row)




    def on_clear_all(self):
        self.history_manager_converter = HistoryManager("converter")
        self.history_manager_todo = HistoryManager("todo")
        self.history_manager_notes = HistoryManager("notes")
        self.history_manager_downloader = HistoryManager("downloader")

        self.history_manager_converter.clear_history()
        self.history_manager_todo.clear_history()
        self.history_manager_notes.clear_history()
        self.history_manager_downloader.clear_history()

        self.load_history_items()





    def on_clear_item(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        id_item = data['item_id']
        tool = data['tool']

        self.history_manager = HistoryManager(tool)

        self.history_manager.delete_record(id_item)

        self.load_history_items()



        





