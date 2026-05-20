import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout,\
 QStackedWidget, QPushButton, QWidget, QDesktopWidget

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from desktop.windows.converter_window import ConverterWindow
from desktop.windows.downloader_window import DownloaderWindow
from desktop.windows.notes_window import NotesWindow
from desktop.windows.todo_window import TodoWindow
from desktop.windows.history_window import HistoryWindow

main_app_icon_path = r"utilityhub\assets\black_spider_icon.png"

class UtilityHubDashboard(QMainWindow):

    def __init__(self):
        super().__init__()
        # customize the main window:
        self.setWindowTitle("UtilityHub")

        screen = QDesktopWidget().screenGeometry() # 2880x1800 (width x height) for me
        app_width = 1700
        app_height = 1100

        x = (screen.width() - app_width) // 2
        y = (screen.height() - app_height) // 2
        
        self.setGeometry(x, y, app_width, app_height)

        self.setWindowIcon(QIcon(main_app_icon_path))
        
        self.initUI()
    
    def initUI(self):
        # -------------------- App Frame ------------------------------------

        """
        u can add a layout manager to mainWindow object, because it has it's own layout stucture incompatible with these 
        # layout managers

        solution: generic widget and add a layout manager to this widget and then add that widget to the main window.
        """
        
        # Central widget:
        self.central_widget = QWidget()
        self.central_widget.setLayout(QVBoxLayout())
        self.setCentralWidget(self.central_widget)


        # ----------------- Tab bar -----------------------------------------



        # Create the tab_bar btns
        self.btn_converter = QPushButton(" Converter")
        self.btn_downloader = QPushButton(" Downloader")
        self.btn_notes = QPushButton(" Notes")
        self.btn_todo = QPushButton(" Todo")
        self.btn_history = QPushButton(" History")

        self.btn_converter.setIcon(QIcon(r"utilityhub\assets\active_tab_btns\swap_active.png"))
        self.btn_converter.setIconSize(QSize(21, 21))

        self.btn_downloader.setIcon(QIcon(r"utilityhub\assets\inactive_tab_btns\down_arrow.png"))
        self.btn_downloader.setIconSize(QSize(18, 18))

        self.btn_notes.setIcon(QIcon(r"utilityhub\assets\inactive_tab_btns\notes_icon.png"))
        self.btn_notes.setIconSize(QSize(18, 18))

        self.btn_todo.setIcon(QIcon(r"utilityhub\assets\inactive_tab_btns\check_box_icon.png"))
        self.btn_todo.setIconSize(QSize(18, 18))

        self.btn_history.setIcon(QIcon(r"utilityhub\assets\inactive_tab_btns\history_icon.png"))
        self.btn_history.setIconSize(QSize(18, 18))



        # Create the tab_bar_layout + add btns to it
        self.tab_bar = QHBoxLayout()
        self.tab_bar.addWidget(self.btn_converter)
        self.tab_bar.addWidget(self.btn_downloader)
        self.tab_bar.addWidget(self.btn_notes)
        self.tab_bar.addWidget(self.btn_todo)
        self.tab_bar.addWidget(self.btn_history)


        # add the tab_bar to the central_widget:
        self.central_widget.layout().addLayout(self.tab_bar)



        # ------------------------- Pages (Content Area) --------------------

        """
        The QStackedWidget class in the Qt Widgets module provides a way to create 
        a user interface with multiple "pages", where only one page (child widget) 
        is visible at a time.
        """

        # Create content_area pages 
        self.page_converter = ConverterWindow()
        self.page_downloader = DownloaderWindow()
        self.page_notes = NotesWindow()
        self.page_todo = TodoWindow()
        self.page_history = HistoryWindow()

        # Create the content_area Widget and add pages to it:
        self.content_area = QStackedWidget()

        self.content_area.addWidget(self.page_converter)  # This is Index 0
        self.content_area.addWidget(self.page_downloader) # Index 1
        self.content_area.addWidget(self.page_notes)      # Index 2
        self.content_area.addWidget(self.page_todo)       # Index 3
        self.content_area.addWidget(self.page_history)    # Index 4


        # add checkable feature:
        for btn in [self.btn_converter, self.btn_downloader, self.btn_notes, self.btn_todo, self.btn_history]:
            btn.setCheckable(True)

        # set default page:
        self.btn_converter.setChecked(True)



        # Action listeners:
        """
        self._change_CurrentIndex(0) if you try to create a function for that,
        it will be executed immediatly so lambda is the right solution for 
        action listeners.
        """
        self.btn_converter.clicked.connect(lambda: self._change_page(0))
        self.btn_downloader.clicked.connect(lambda: self._change_page(1))
        self.btn_notes.clicked.connect(lambda: self._change_page(2))
        self.btn_todo.clicked.connect(lambda: self._change_page(3))
        self.btn_history.clicked.connect(lambda: self._change_page(4))


        # add the stacked widget to central_widget
        self.central_widget.layout().addWidget(self.content_area)






        # tell the window to create a status bar:
        self.statusBar().showMessage("Ready")




        # ------------------------- Styling (css) ------------------------------

        self.btn_converter.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_downloader.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_history.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_notes.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_todo.setCursor(Qt.CursorShape.PointingHandCursor)


        self.btn_converter.setObjectName("tab")
        self.btn_downloader.setObjectName("tab")
        self.btn_history.setObjectName("tab")
        self.btn_notes.setObjectName("tab")
        self.btn_todo.setObjectName("tab")



        ## ----------------- tab bar styling ----------------------------
        self.setStyleSheet("""
            QPushButton#tab {
                background: transparent;
                color: #a0a0a0;     /* Gray text */
                border: none;       /* Remove standard ugly button edges */
                font-size: 18px;
                padding: 10px;
            }
            
            QPushButton#tab:hover {
                color: #ffffff;     /* White text on hover */
                font-size:19px;
            }
            
            QPushButton#tab:checked {
                color: #4da6ff;     /* Blue text */
                font-size:22px;
                border-bottom: 2px solid #4da6ff;  /* Blue underline */
            }
        """)




    def _change_page(self, index):
        self.content_area.setCurrentIndex(index)

        inactive_icons = [
            r"utilityhub\assets\inactive_tab_btns\swap_icon.png",
            r"utilityhub\assets\inactive_tab_btns\down_arrow.png",
            r"utilityhub\assets\inactive_tab_btns\notes_icon.png",
            r"utilityhub\assets\inactive_tab_btns\check_box_icon.png",
            r"utilityhub\assets\inactive_tab_btns\history_icon.png"
        ]
        
        active_icons = [
            r"utilityhub\assets\active_tab_btns\swap_active.png",
            r"utilityhub\assets\active_tab_btns\down_arrow_Active.png",
            r"utilityhub\assets\active_tab_btns\notes_active.png",
            r"utilityhub\assets\active_tab_btns\checkbox_active.png",
            r"utilityhub\assets\active_tab_btns\history_active.png"
        ]


        btns = [self.btn_converter, self.btn_downloader, self.btn_notes, self.btn_todo, self.btn_history]




        for i, btn in enumerate(btns):
            is_active = (index == i)
            btn.setChecked( is_active )

            btn.setIcon(QIcon(active_icons[i])) if is_active else btn.setIcon(QIcon(inactive_icons[i]))
            btn.setIconSize(QSize(21, 21)) if is_active else btn.setIconSize(QSize(18, 18))


        if index == 4:
            # history code:
            self.page_history.load_history_items()