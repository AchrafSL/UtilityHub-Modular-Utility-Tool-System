import sys
from PyQt5.QtWidgets import QApplication 
from desktop.main_window import UtilityHubDashboard

def main():
    app = QApplication(sys.argv)

    # Global css
    app.setStyleSheet("""
        QMainWindow, QStackedWidget {
            background-color: #1a1a18;
        }
                      
        /* label css */
        QLabel {
            color: #9c9a92;
            font-family: 'Consolas', monospace;
            font-weight: bold;
        }
                      
        QLineEdit, QComboBox, QTextEdit {
            background-color: #272724;
            border: 1px solid #3a3a36;
            border-radius: 6px;
            padding: 8px;
            color: #e8e6de;
        }
                      
        QPushButton {
            background-color: #272724;
            border: 1px solid #3a3a36;
            border-radius: 6px;
            padding: 8px 16px;
            color: #e8e6de;
        }
                      
        QPushButton:hover {
            border-color: #85b7eb;
            color: #85b7eb;
        }


        QPushButton#convert_btn {   
            background-color: #1f4068; 
            color: #cbd5e0;          
            border: none;
            padding: 12px 25px;
            border-radius: 18px;
        }

        QPushButton#convert_btn:disabled {   
            background-color: #1a242f; 
            color: #3f4e5c;           
        }
       
        QPushButton#convert_btn:hover {
            background-color: #2c5282;
        }




        /* list widget css */
        QListWidget {
            background-color: transparent;
            border: none;
            color: #8b949e;
            outline: 0;

        }

        QListWidget::item {
            background-color: transparent;
            margin-bottom: 8px; 
            padding: 0px;
        }
        
        /* remove the blue hover background */
        QListWidget::item:hover {
            background-color: transparent;
        }
        
        /*  remove the blue selection background  */
        QListWidget::item:selected {
            background-color: transparent;
            outline: none;
        }
        
        /* scrollbar css */
        QScrollBar:vertical {
            border: none;
            background: #1e1e1c;
            width: 8px;
            margin: 0px;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical {
            background: #3a3a36;
            min-height: 20px;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical:hover {
            background: #8b949e;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }

        QScrollBar:horizontal {
            border: none;
            background: #1e1e1c;
            height: 8px;
            margin: 0px;
            border-radius: 4px;
        }
        QScrollBar::handle:horizontal {
            background: #3a3a36;
            min-width: 20px;
            border-radius: 4px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #8b949e;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        



        /* card css */
        QFrame#card {
            background-color: #1e1e1c;
            border: 1px solid #3a3a36;
            border-radius: 12px;
            padding: 8px;
        }

        /* card titles css */
        QLabel#card_title {
            color: #8b949e;
            border-bottom: 1.5px solid #3a3a36; 
            padding-bottom: 8px;
            border-radius: 0px;
        }



        /* danger button css */
        QPushButton#danger_btn {
            background-color: #272724;
            border: 1.5px solid #5c3535;
            color: #f09595;
            padding: 6px 12px;
        }
        
        QPushButton#danger_btn:hover {
            background-color: #3b2a2a;
            border-color: #f09595;
            color: #ffffff;
        }

        QPushButton#card_download_btn {
             background-color: #0b3d66;
             font-family: Arial;
             color: #85b7eb;
             border: none;
             padding: 8px;
             font-weight: bold;
             border-radius: 6px;
        }

        QPushButton#card_download_btn:hover {
             background-color: #1a4a6e;
             color: #ffffff;
        }

        QPushButton#card_download_btn[type="audio"] {
             background-color: #6e4a1a;
             color: #f6ad55;
        }

        QPushButton#card_download_btn[type="audio"]:hover {
             background-color: #8a5c21;
             color: #ffffff;
        }

                      
        /* results format cards css */
        QFrame#format_card {
            background-color: #1e1e1c;
            border: 1.5px solid #3a3a36;
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 8px;
        }

        QFrame#format_card[type="video"] {
            border-color: #1a4a6e;
        }

        QFrame#format_card[type="video"]:hover {
            border-color: #3182ce;
        }

        QFrame#format_card[type="audio"] {
             border-color: #6e4a1a;
        }

        QFrame#format_card[type="audio"]:hover {
            border-color: #ce8231;
        }

        QLabel#card_type_title {
            font-size: 30px;
            font-weight: bold;
            color: #e8e6de;
        }

        QLabel#card_type_title[type="video"] {
            color: #63b3ed;
        }

        QLabel#card_type_title[type="audio"] {
            color: #f6ad55;
        }

        QLabel#card_details {
            color: #9c9a92;
            font-size: 20px;
        }

        /* scroll area css */
        QScrollArea {
            background-color: transparent;
            border: none;
            margin-top: 20px;
        }

        QScrollArea > QWidget > QWidget#result_content {
            background-color: transparent;
        }



        QComboBox {
            background-color: #1A1A18;
            color: #d1d5db;
            border: 1px solid #3a3a36;
            border-radius: 6px;
            padding: 6px 12px;
        }

        QComboBox::drop-down {
            border-left: 1px solid #3a3a36;
            width: 25px;
        }

        /* css for drowdown menu */
        QComboBox QAbstractItemView {
            background-color: #1A1A18;
            color: #d1d5db;
            border: 1px solid #3a3a36;
            selection-background-color: #1f6feb;
            selection-color: white;
            outline: none; 
        }




        #tag_btn {
            background-color: #272724;
            color: #E8E6DE;
            border: 1px solid #3a3a36;
            border-radius: 12px; 
            padding: 4px 12px;
        }

        #tag_btn:hover {
            border: 1px solid #8b949e;
            color: white;
        }

        #tag_btn:checked {
            background-color: #042C53;
            border: 1px solid #52a8ff; 
            color: #85B7EB;
        }


        #success_btn {
            background-color: #04342C;
            color: #5DCAA5;
            border: 1px solid #5DCAA5;
            border-radius: 6px;
            padding: 6px 12px;
            font-weight: bold;
        }
        #success_btn:hover {
            background-color: #064d42; 
        }


        #danger_note {
            background-color: #501313;
            color: #F09584;
            border: 1px solid #F09584;
            border-radius: 6px;
            padding: 6px 12px;
            font-weight: bold;
        }
        #danger_note:hover {
            background-color: #6a1a1a;
        }




        #notes_list {
            background-color: transparent;
            border: none;
            outline: none; 
        }

        #notes_list::item {
            background-color: transparent;
            border: 1px solid #3a3a36;
            border-radius: 8px;
        }

        #notes_list::item:hover {
            background-color: #272724;
            border: 1px solid #8b949e;
        }

        #notes_list::item:selected {
            background-color: #042C53; 
            border: 1px solid #52a8ff; 
        }


        /* task window */
        QLabel#count_badge {
            color: #85b7eb;
            background-color: #042C53;
            border: 1px solid #1f6feb;
            border-radius: 8px;
            padding: 1px 8px;
            font-size: 16px;
        }

        QLabel#filter_count {
            color: #5DCAA5;
            font-style: italic;
            font-size: 19px;
            margin-top: 10px;
        }

        QPushButton#todo_add_btn {
            background-color: #72a8e8;
            color: #ffffff;
            border: none;
            border-radius: 12px;
            padding: 10px;
            font-weight: bold;
            font-size: 14px;
        }

        QPushButton#todo_add_btn:hover {
            background-color: #85b7eb;
        }

        QComboBox#task_status_dropdown {
            background-color: #272724;
            border: 1px solid #3a3a36;
            border-radius: 6px;
            padding: 2px 8px;
            font-size: 16px;
            color: #e8e6de;
        }

        QComboBox#task_status_dropdown[status="Pending"] {
            color: #f6ad55;
            border-color: #6e4a1a;
        }

        QComboBox#task_status_dropdown[status="In-progress"] {
            color: #85b7eb;
            border-color: #1f6feb;
        }

        QComboBox#task_status_dropdown[status="Done"] {
            color: #5DCAA5;
            border-color: #1a6e4a;
        }

        QLabel#section_title {
            color: #8b949e;
            font-size: 18px;
            letter-spacing: 1.5px;
            font-weight: bold;
        }

        #task_content {
            background-color: transparent;
            border: none;
            color: #e8e6de;
            font-size: 22px;
            font-family: 'Segoe UI', Arial;
        }

        QCheckBox::indicator {
            width: 22px;
            height: 22px;
        }

                      

        /* history css*/
        #history_list {
            background-color: transparent;
            outline: none; 
        }

        #history_list::item {
            background-color: #272724;
            border: 1px solid #3a3a36;
            margin-bottom:0px;
        }

  


        #history_card {
            background-color: #1e1e1c;
            border: 1px solid #3a3a36;
            border-radius: 12px;
        }


    """)






    window = UtilityHubDashboard()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
