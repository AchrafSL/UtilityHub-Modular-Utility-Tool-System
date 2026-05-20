import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout \
    , QPushButton, QLabel, QWidget, QLineEdit, QComboBox, QTextEdit, QListWidget, \
        QListWidgetItem, QFrame, QFileDialog

from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from modules.converter.converter_service import ConverterService

import os

class ConverterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.converter_service = ConverterService()
        self.converter_service._refresh_settings()
        self.initUI()


    def initUI(self):
        self.master_H_layout = QHBoxLayout()
        # applies the master layout to the QWidget page
        self.setLayout(self.master_H_layout) 

        self.left_card_frame = QFrame()
        self.left_V_layout = QVBoxLayout(self.left_card_frame)
        """
        This self.left_V_layout = QVBoxLayout(self.left_card_frame) is the same as:

        self.left_V_layout = QVBoxLayout()
        self.left_card_frame.setLayout(self.left_V_layout)

        When using layouts, always add child widgets to the layout.
        The frame is the container that holds the layout and allows styling and structure.
        """

        self.right_V_layout = QVBoxLayout()

        """
        Because u can't apply css to layouts, I used QFrames.
        Also layout have an invisible margin, because of that nested layouts
         make UI bugs -> solution: set them to 0 from the start.

        """
        
        # -------------------- left card ---------------------------------

        # left card components:

        ## Card Title
        self.left_card_title = QLabel("INPUT FILE")

        ## source_file
        self.source_file_label = QLabel("Source file — browse or drag")
        self.source_file_lineedit = QLineEdit()
        self.source_file_lineedit.setPlaceholderText("No file selected")
        self.source_file_lineedit.setDisabled(True)
        self.source_file_button = QPushButton("Browse...")
        self.source_file_button.clicked.connect(self.choose_source_file)

        self.source_row1 = QHBoxLayout()
        self.source_row1.setContentsMargins(0, 0, 0, 0)
        self.source_row1.addWidget(self.source_file_lineedit)
        self.source_row1.addWidget(self.source_file_button) 



        ## output_format
        self.output_format_label = QLabel("Output format")
        self.output_format_dropdown = QComboBox()
        self.output_format_dropdown.addItem("Select a file first")
        self.output_format_dropdown.setDisabled(True)

        

        ## Save to — output_path 
        self.save_to_label = QLabel("Save to — output_path")
        self.save_to_lineedit = QLineEdit()
        self.save_to_lineedit.setPlaceholderText(self.converter_service.output_path)
        self.save_to_lineedit.setDisabled(True)
        self.save_to_button = QPushButton("Browse...")
        self.save_to_button.clicked.connect(self.choose_save_folder)

        self.save_to_row1 = QHBoxLayout()
        self.save_to_row1.setContentsMargins(0, 0, 0, 0)
        self.save_to_row1.addWidget(self.save_to_lineedit)
        self.save_to_row1.addWidget(self.save_to_button)


        # Convert button:
        self.btn_convert = QPushButton("Convert")
        self.btn_convert.setDisabled(True)
        self.btn_convert.clicked.connect(self.start_conversion)


        # Add Created widgets to the left card
        self.left_V_layout.addWidget(self.left_card_title)

        self.left_V_layout.addWidget(self.source_file_label)
        self.left_V_layout.addLayout(self.source_row1)

        self.left_V_layout.addWidget(self.output_format_label)
        self.left_V_layout.addWidget(self.output_format_dropdown)

        self.left_V_layout.addWidget(self.save_to_label)
        self.left_V_layout.addLayout(self.save_to_row1)

        self.left_V_layout.addWidget(self.btn_convert)
        


        # ------------------------------- Right Card --------------------------
        
        ## top card (Output log) -------------------------------------------
        self.top_right_card_frame = QFrame()
        self.top_right_card = QVBoxLayout(self.top_right_card_frame)
        self.top_right_card_frame.setFixedHeight(250)

        
        ### top card components:
        self.log_label = QLabel("OUTPUT LOG")
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setPlaceholderText("Waiting for instructions...")
        self.log_console.setStyleSheet("background-color:#1A1A18")

        ### add components to top card:
        self.top_right_card.addWidget(self.log_label)
        self.top_right_card.addWidget(self.log_console)


        ## bottom card (Recent conversions) ------------------------------
        self.bottom_right_card_frame = QFrame()
        self.bottom_right_card = QVBoxLayout(self.bottom_right_card_frame)

        ### bottom card components:
        self.recent_label = QLabel("Recent Conversions")
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_recent_list)


        self.hr_line = QFrame()
        self.hr_line.setFixedHeight(1)
        self.hr_line.setStyleSheet("background-color: #3a3a36; border: none;")
        


        self.bottom_card_title_row = QHBoxLayout()
        self.bottom_card_title_row.addWidget(self.recent_label)
        self.bottom_card_title_row.addStretch()
        self.bottom_card_title_row.addWidget(self.clear_btn)


        self.recent_list = QListWidget()
        self.recent_list.setSpacing(8) # 8px top-margin between every row!
        self.recent_list.setFixedHeight(250)
        self.recent_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        ### load list:
        self.populate_list()

        ### Add components to bottom card:
        self.bottom_right_card.addLayout(self.bottom_card_title_row)
        self.bottom_right_card.addWidget(self.hr_line)
        self.bottom_right_card.addWidget(self.recent_list)






    
        ## add subCards to right card:
        self.right_V_layout.addWidget(self.top_right_card_frame)
        self.right_V_layout.addWidget(self.bottom_right_card_frame)

        ## add auto adjust to content :
        self.right_V_layout.addStretch()
        
        self.right_widget_container = QWidget()
        self.right_widget_container.setLayout(self.right_V_layout)


        # Add cards to main layout:
        self.master_H_layout.addWidget(self.left_card_frame, alignment= Qt.AlignmentFlag.AlignTop)
        self.master_H_layout.addWidget(self.right_widget_container, alignment= Qt.AlignmentFlag.AlignTop)

        



        # -------------------------- Styling (css) -------------------------
        
        ## giving ids:
        self.left_card_frame.setObjectName("card")
        self.top_right_card_frame.setObjectName("card")
        self.bottom_right_card_frame.setObjectName("card")

        self.left_card_title.setObjectName("card_title")
        self.log_label.setObjectName("card_title")
        self.recent_label.setStyleSheet("color: #8b949e;")

        self.btn_convert.setObjectName("convert_btn")
        self.clear_btn.setObjectName("danger_btn")


        # ----------------------- padding/Margins -----------------------------

        # for layouts: margins already set to (0,0,0,0) except right_V_layout
 
        # inner_padding for frames 
        self.left_V_layout.setContentsMargins(16, 16, 16, 16)
        self.top_right_card.setContentsMargins(16, 16, 16, 16)
        self.bottom_right_card.setContentsMargins(16, 16, 16, 16)

        # gap between widgets
        self.left_V_layout.setSpacing(12) 

        # gap between right and left cards
        self.master_H_layout.setSpacing(24)
        # gap between top and bottom right cards
        self.right_V_layout.setSpacing(24)

        
        # Delete invisible margin for right_V_layout and add bottom-padding for <hr>
        self.right_V_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_card_title_row.setContentsMargins(0, 0, 0, 8) 


        # -------------- mouse cursor hover effect ---------------------------

        self.btn_convert.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.source_file_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_to_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.output_format_dropdown.setCursor(Qt.CursorShape.PointingHandCursor)




    def choose_source_file(self):
        file_filter = (
            "Supported Files (*.png *.jpg *.jpeg *.bmp *.tiff *.md *.mp4 *.webp);;"
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff *.webp);;"
            "Markdown Files (*.md);;"
            "Video Files (*.mp4);;"
            "All Files (*)"
        )


        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Convert", "", file_filter)
        # _ is file_type eg("Text Files (*.txt)" ..)

        if file_path:
            self.source_file_lineedit.setText(file_path)

            ext = os.path.splitext(file_path)[1].lower()

            self.update_available_format(ext)



    def start_conversion(self):
        file_path = self.source_file_lineedit.text()
        ext_to_convert = self.output_format_dropdown.currentText()

        self.btn_convert.setDisabled(True)
        self.btn_convert.setText("Converting...")
        self.source_file_button.setDisabled(True)
        self.save_to_button.setDisabled(True)

        self.log_console.setText(f"Processing: Transforming to {ext_to_convert}...")

        


        self.converterWorker = ConverterWorker(ext_to_convert, file_path, self.converter_service)
        self.converterWorker.finished.connect(self.on_finish_received)
        self.converterWorker.start()




    def on_finish_received(self, status):
    
        self.btn_convert.setDisabled(False)
        self.btn_convert.setText("Convert")
        self.source_file_button.setDisabled(False)
        self.save_to_button.setDisabled(False)
        if status == 1:
            self.log_console.setText("Success: File converted successfully!")
            self.populate_list()
            
            print("conversion finished successfully!")
        else:
            self.log_console.setText("Error: Conversion failed. See terminal for details.")
            print("Convertion FAILED!")


    def update_available_format(self, ext):
        self.output_format_dropdown.clear()
        self.output_format_dropdown.setDisabled(True)


        formats_map = {
            '.md': ['PDF'],
            '.mp4': ["MP3"],
            ".png": ["JPG", "SVG"],  
            ".jpg": ["PNG", "SVG"],  
            ".jpeg": ["PNG", "SVG"], 
            ".webp": ["JPG", "PNG", "SVG"], 
            ".bmp": ["JPG", "PNG"],  
            ".tiff": ["JPG"]      
        }

        available_formats = formats_map.get(ext, [])

        if available_formats:
            self.output_format_dropdown.addItems(available_formats)
            self.output_format_dropdown.setDisabled(False)
            self.btn_convert.setDisabled(False)
            
        else:
            self.output_format_dropdown.addItem("ext Not supported ")
            self.output_format_dropdown.setDisabled(True)



        

    def choose_save_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            self.converter_service.output_path # for default path
        )

        if folder_path:
            self.save_to_lineedit.setText(folder_path)
            self.converter_service.settingsManager.update_setting("output_paths","converter", folder_path)


    
    def populate_list(self):        
        self.recent_list.clear() # Clear the UI only 

        list_of_recent_conversions = self.converter_service.historyManager.get_history()

      
        for index, l in list_of_recent_conversions.iterrows(): # that's a common way to iterate over a pandas df
            outFile = l['Response']

            if not os.path.exists(outFile):
                continue # file gone, don't show it

            folder_location = os.path.dirname(outFile)
            ext = os.path.splitext(outFile)[1].replace(".", "").upper()
            filename = os.path.basename(outFile)


            # because Qwidget dont have addWidget only layout have it
            # solution is row_widget.layout().addWidget

            # get empty container from recent_list:
            item = QListWidgetItem(self.recent_list)

            row_widget = QWidget()
            row_widget.setLayout(QHBoxLayout())
            row_widget.layout().addSpacing(16) 

            
            outformat_label = QLabel(f"{ext}")
            

            # -- periodic color change:
            if index % 2 == 0: 
                outformat_label.setStyleSheet("background-color: #052440; color: #52a8ff; border-radius: 12px; font-weight: bold; padding: 4px 12px;")
            else:               
                outformat_label.setStyleSheet("background-color: #402305; color: #ff9100; border-radius: 12px; font-weight: bold; padding: 4px 12px;")


            
            outFileName_label = QLabel(f"{filename}")
            outFileName_label.setFixedWidth(240)
            outFileName_label.setWordWrap(True)
            outFileName_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)



            btn_download = QPushButton(" Open Folder")
            btn_download.clicked.connect(lambda _, path=folder_location: os.startfile(path))
            btn_del = QPushButton(" Delete")
            btn_del.clicked.connect(lambda _,log_id=index, filepath = outFile: self.delete_file(log_id, filepath) )

            # buttons styling: (icons)
            btn_download.setIcon(QIcon(r"utilityhub\assets\blue_download_icon.png"))
            btn_download.setIconSize(QSize(18, 18)) 

            btn_del.setObjectName("danger_btn")  
            btn_del.setIcon(QIcon(r"utilityhub\assets\red_X_icon.png"))
            btn_del.setIconSize(QSize(18, 18))




            # adding components to widget:
            row_widget.layout().addWidget(outformat_label, alignment=Qt.AlignmentFlag.AlignVCenter)
            row_widget.layout().addWidget(outFileName_label, alignment=Qt.AlignmentFlag.AlignVCenter)
            row_widget.layout().addWidget(btn_download, alignment=Qt.AlignmentFlag.AlignVCenter)
            row_widget.layout().addWidget(btn_del, alignment=Qt.AlignmentFlag.AlignVCenter)


            # mouse cursor effect
            btn_download.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)

            # delete invisible padding
            row_widget.layout().setContentsMargins(0, 0, 0, 0)
            
            # --- Container with Separator (HR) ---
            hr = QFrame()
            hr.setFixedHeight(1)
            hr.setStyleSheet("background-color: #3a3a36; border: none;")

            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(8)
            
            container_layout.addWidget(row_widget)
            container_layout.addWidget(hr)

            ## Fuse the widget into the blank list item!
            # customize the size of the row to fit the content
            item.setSizeHint(container.sizeHint()) 
            self.recent_list.setItemWidget(item, container)



    def delete_file(self, log_id, filepath):
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            pass

        self.converter_service.historyManager.delete_record(log_id) 
        self.populate_list() 
        self.log_console.setText("File removed.")




    def clear_recent_list(self):
        self.converter_service.historyManager.clear_history() 
        self.populate_list() 
        self.log_console.setText(" History cleared (Converted files were NOT deleted).")


class ConverterWorker(QThread):
    """
     this one does hard math (CPU bound) so it might freeze the UI
      for a second while it's doing it's work.
    """
    finished = pyqtSignal(int)
    def __init__(self, ext, input_path, service):
        super().__init__()
        self.ext = ext
        self.input_path = input_path
        self.service = service


    def run(self):
        try:
            input_ext = os.path.splitext(self.input_path)[1].lower()
            match(self.ext):
                case "PDF": 
                    if input_ext == ".md":
                        self.service.convert_md_to_pdf(self.input_path)
                    elif input_ext == ".txt":
                        self.service.convert_txt_to_pdf(self.input_path)
                case "MP3": self.service.convert_mp4_to_mp3(self.input_path)
                case "SVG": self.service.convert_to_svg(self.input_path)
                case "JPG": self.service.convert_to_jpg(self.input_path)
                case "PNG": self.service.convert_to_png(self.input_path)
                case _: print("ext not supported")

            self.finished.emit(1)

        except Exception as e:
            print(f"Converter service ERROR: {e}")
            self.finished.emit(-1)


        
        
