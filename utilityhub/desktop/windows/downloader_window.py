
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel \
    , QLineEdit, QPushButton, QListWidget, QListWidgetItem \
        , QScrollArea, QTextEdit, QFileDialog

from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal

from PyQt5.QtGui import QIcon

from modules.downloader.downloader_service import MediaDownloaderService

import os
import glob 
import time

class DownloaderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.download_service = MediaDownloaderService()
        self.download_queue = []


        self.is_currently_downloading = False # to check for when the next worker arrive
        self.nbr_of_downloads = 0
        self.queue_refs = {} # to store queue labels to change them later 


        self.download_service._refresh_settings()

        self.initUI()


    def initUI(self):
        self.master_H_layout = QHBoxLayout()
        self.setLayout(self.master_H_layout)

        # 1. left card: -----------------------------------------
        self.left_card = QFrame()
        self.left_card.setLayout(QVBoxLayout())
        self.left_card.setObjectName("card")
        """
        Ways to work:
        
        Case1:
                self.left_card = QFrame()
                self.left_card.setLayout(QVBoxLayout())

            and use .layout() to add layouts + widgets:
                self.left_card.layout().addWidget(smth)
        
        --------------------------------------------------

        Case2:
                self.left_card = QFrame()
                self.left_card_layout = QVBoxLayout(self.left_card)

            and add widgets and layouts normally:
                self.left_card_layout.addWidget(smth)

        """




        # 2. right layout -----------------------------------------
        """no need to use QWidget because, i dont want to control
         whole right UI"""
        self.right_layout = QVBoxLayout()

        ## 2.1. top right card
        self.top_right_card = QFrame()
        self.top_right_card.setLayout(QVBoxLayout())
        self.top_right_card.setObjectName("card")

        ## 2.2. bottom right card
        self.bottom_right_card = QFrame()
        self.bottom_right_card.setLayout(QVBoxLayout())
        self.bottom_right_card.setObjectName("card")





        # 4. Custom left card ------------------------------------

        ## 4.1. delete invisible spaces:
        self.left_card.layout().setContentsMargins(0, 0, 0, 0)
        self.left_card.layout().setSpacing(0)

        ## 4.2. Title:
        self.video_title = QLabel("VIDEO URL")
        self.video_title.setObjectName("card_title")
        self.video_title.setStyleSheet("padding-left:16px; padding-top:16px;")

        ## 4.3. Hr line:
        self.hr_line = QFrame()
        self.hr_line.setFixedHeight(1)
        self.hr_line.setStyleSheet("background-color: #3a3a36; border: none;")

        ## 4.4. left_body
        self.left_body_container = QVBoxLayout()
        self.left_body_container.setContentsMargins(16, 8, 16, 16)
        self.left_body_container.setSpacing(8)


        #### formats area:
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True) 
        self.scroll_area.setMinimumHeight(600)

        self.result_content_widget = QWidget()
        self.result_content_widget.setObjectName("result_content")

        self.result_content_widget.setLayout(QVBoxLayout())

        self.scroll_area.setWidget(self.result_content_widget)

        self.scroll_area.hide()



        ### 4.4.1 add content to left_body:

        #### part1
        self.url_label = QLabel("URL")

        self.url_row = QHBoxLayout()
        self.url_row.setContentsMargins(0, 0, 0, 0)
        self.url_lineedit = QLineEdit()
        self.url_lineedit.setPlaceholderText("https://youtube.com/watch?v=...")
        self.fetch_btn = QPushButton("Fetch")
        self.clear_fetch_btn = QPushButton("Clear")
        self.clear_fetch_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_fetch_btn.setObjectName("danger_btn")
        self.clear_fetch_btn.hide()
        self.clear_fetch_btn.clicked.connect(lambda : self.clear_fetch_btn_called())

        self.fetch_btn.clicked.connect(self.start_fetching)

        self.url_row.addWidget(self.url_lineedit)
        self.url_row.addWidget(self.fetch_btn)
        self.url_row.addWidget(self.clear_fetch_btn)


        #### part2
        self.save_to_label = QLabel("SAVE TO - OUTPUT PATH")


        self.save_to_row = QHBoxLayout()
        self.save_to_row.setContentsMargins(0, 0, 0, 0)
        self.save_to_lineedit = QLineEdit()
        self.save_to_lineedit.setPlaceholderText(self.download_service.output_path)
        self.save_to_lineedit.setDisabled(True)
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.choose_save_folder)

        self.save_to_row.addWidget(self.save_to_lineedit)
        self.save_to_row.addWidget(self.browse_btn)

        #### add components to the left body container:
        self.left_body_container.addWidget(self.url_label)
        self.left_body_container.addLayout(self.url_row)
        self.left_body_container.addWidget(self.save_to_label)
        self.left_body_container.addLayout(self.save_to_row)
        self.left_body_container.addWidget(self.scroll_area)




        ## 4.5. add the 3 parts to the left card:
        self.left_card.layout().addWidget(self.video_title)
        self.left_card.layout().addWidget(self.hr_line)
        self.left_card.layout().addLayout(self.left_body_container)




        # 5. Right-Side ------------------------------------------------------

        ## 5.1 top-right side -----------------------------------------------

        ### 5.1.1. delete invisible spaces
        self.top_right_card.layout().setContentsMargins(0, 0, 0, 0)
        self.top_right_card.layout().setSpacing(0)

        ### 5.1.2. Title:
        self.queue_title = QLabel("QUEUE")
        self.queue_title.setObjectName("card_title")
        self.queue_title.setStyleSheet("padding-left:16px; padding-top:16px;")


        ### 5.1.3. <Hr>
        self.hr_line_queue = QFrame()
        self.hr_line_queue.setFixedHeight(1)   
        self.hr_line_queue.setStyleSheet("background-color: #3a3a36; border: none;")


        ### 5.1.4. top_right_body_container
        self.top_right_body_container = QVBoxLayout()
        self.top_right_body_container.setContentsMargins(16, 8, 16, 16)
        self.top_right_body_container.setSpacing(8)


        ### 5.1.5. add content to the container:
        self.queue_list = QListWidget()
        self.queue_list.setSpacing(8) # 8px between items
        self.queue_list.setFixedHeight(250)
        self.queue_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.top_right_body_container.addWidget(self.queue_list)





        ### 5.1.6. add the parts to the top right card:
        self.top_right_card.layout().addWidget(self.queue_title)
        self.top_right_card.layout().addWidget(self.hr_line_queue)
        self.top_right_card.layout().addLayout(self.top_right_body_container)




        ## 5.2 bottom right card: -----------------------------------------


        ### 5.2.1. delete invisible spaces
        self.bottom_right_card.layout().setContentsMargins(0, 0, 0, 0)
        self.bottom_right_card.layout().setSpacing(0)

        ### 5.2.2. Title:
        self.log_title = QLabel("OUTPUT LOG")
        self.log_title.setObjectName("card_title")
        self.log_title.setStyleSheet("padding-left:16px; padding-top:16px;")


        ### 5.2.3. <Hr>
        self.hr_line_log = QFrame()
        self.hr_line_log.setFixedHeight(1)   
        self.hr_line_log.setStyleSheet("background-color: #3a3a36; border: none;")


        ### 5.2.4. bttom_right_body_container
        self.bottom_right_body_container = QVBoxLayout()
        self.bottom_right_body_container.setContentsMargins(16, 8, 16, 16)
        self.bottom_right_body_container.setSpacing(8)


        ### 5.2.5. add content to the container:
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setPlaceholderText("Waiting for instructions...")
        self.log_console.setStyleSheet("background-color:#1A1A18")

        self.bottom_right_body_container.addWidget(self.log_console)



        ### 5.2.6. add the parts to the top right card:
        self.bottom_right_card.layout().addWidget(self.log_title)
        self.bottom_right_card.layout().addWidget(self.hr_line_log)
        self.bottom_right_card.layout().addLayout(self.bottom_right_body_container)







        # ------------------------- Styling (CSS) -------------------------------



        # gap between widgets
        self.left_card.layout().setSpacing(12) 

        # gap between right and left cards
        self.master_H_layout.setSpacing(24)

        # gap between top and bottom right cards
        self.right_layout.setSpacing(24)


        # Mouse Hover Effect
        for btn in [self.fetch_btn, self.browse_btn]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)









       # finally. add left card and right layout to main layout: -------------

        ## add sub cards to right layout:
        self.right_layout.addWidget(self.top_right_card)
        self.right_layout.addWidget(self.bottom_right_card)

        # push content within the cards to the top
        self.left_card.layout().addStretch() 
        self.top_right_card.layout().addStretch()
        self.bottom_right_card.layout().addStretch()

        # push the two sub cards to the top
        self.right_layout.addStretch() 


        # put everything on the screen
        self.master_H_layout.addWidget(self.left_card, stretch=1, alignment = Qt.AlignmentFlag.AlignTop)
        self.master_H_layout.addLayout(self.right_layout, stretch=1)






    def choose_save_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder",
            self.download_service.output_path # for default path
        )

        if folder_path:
            self.save_to_lineedit.setPlaceholderText(folder_path)
            self.download_service.settingsManager.update_setting("output_paths","downloader", folder_path)


    def clear_fetch_btn_called(self):
        self.clear_fetch_btn.hide()
        self.clear_fetch_results()
        self.url_lineedit.setText("")
        





    def add_queue_row(self,idI, title):
        item = QListWidgetItem(self.queue_list)

        row_widget = QWidget()
        row_widget.setLayout(QHBoxLayout())
        row_widget.layout().addSpacing(16) 

        status = QLabel("Queued")
        status.setStyleSheet("background-color: #501313; color: #FF5252; border-radius: 12px; font-weight: bold; padding: 4px 35px 4px 12px;")


        # save status to change it later when Done:
        self.queue_refs[idI] = status

    
        status.setFixedWidth(150)
        status.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)


        filename = QLabel(f"{title}")
        filename.setAlignment(Qt.AlignmentFlag.AlignCenter)




        cancel_btn = QPushButton("")
        cancel_btn.setIcon(QIcon(r"utilityhub\assets\red_X_icon.png"))
        cancel_btn.setIconSize(QSize(16, 16))
        cancel_btn.setFixedSize(30, 30)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 82, 82, 0.1);
                border-radius: 15px;
            }
        """)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(lambda _ ,idIv=idI, itemv=item: self.cancel_queue_item(idIv, itemv))


        # adding components to widget:
        row_widget.layout().addWidget(status, alignment=Qt.AlignmentFlag.AlignVCenter)
        row_widget.layout().addWidget(filename)  
        row_widget.layout().addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignVCenter)

        # delete invisible padding
        row_widget.layout().setContentsMargins(0, 0, 0, 0)

        # --- Container with Separator (HR) ---
        hr = QFrame()
        hr.setFixedHeight(1)
        hr.setStyleSheet("background-color: #3a3a36; border: none;")

        row_with_hr = QWidget()
        row_with_hr.setLayout(QVBoxLayout())
        row_with_hr.layout().setContentsMargins(0, 0, 0, 0)
        row_with_hr.layout().setSpacing(8)
        row_with_hr.layout().addWidget(row_widget)
        row_with_hr.layout().addWidget(hr)



        ## Fuse the widget into the blank list item!
        # customize the size of the row to fit the content
        item.setSizeHint(row_with_hr.sizeHint()) 
        self.queue_list.setItemWidget(item, row_with_hr)








    def delete_junck(self, path):
        # for both cancel and error -> status: ERROR
        try:

            """
            First solution didn't work because yt-dlp creates files with video.f399.mp4.part etc

            if os.path.exists(path):
                os.remove(path)

            # delete part files:
            base_path = os.path.splitext(path)[0]

            if os.path.exists(base_path + ".part"):
                os.remove(base_path + ".part") 

            if os.path.exists(path + ".part"):
                os.remove(path + ".part") 

            
            Right solution is to use search with * (globbing)
            """

            # wait for yt-dlp to release the file 
            time.sleep(0.1) 


            # delete main file
            if os.path.exists(path):
                os.remove(path)

            # delete partials
            base_path = os.path.splitext(path)[0]

            for file in glob.glob(base_path + "*"):
                if file.endswith(".part"):
                    os.remove(file)
        except:
            print("ERROR WHILE DELETING JUNCK FILES!")





    def cancel_queue_item(self, idI, item):
        # if it's the active -> kill thread
        try:
            if self.is_currently_downloading and self.current_worker_id == idI:
                #self.downloadworker.terminate()
                self.downloadworker.is_killed = True
                self.is_currently_downloading = False
        except:
            pass 


        # if queue -> remove it from list
        try:
            self.download_queue = list( filter(lambda info: info['id'] != idI, self.download_queue) )
            row = self.queue_list.row(item)
            self.queue_list.takeItem(row) # remove item

            # Release formats:
            self.result_content_widget.setDisabled(False)
        except:
            pass

        



    def start_fetching(self):
        self.fetch_btn.setText("Loading...")
        self.current_fetched_url = self.url_lineedit.text()

        self.fetch_btn.setDisabled(True)
        self.url_lineedit.setDisabled(True)

        self.fetchworker = FetchWorker(self.url_lineedit.text(), self.download_service)

        #  call on_received when the signal finished is sent
        self.fetchworker.finished.connect(self.on_received) 

        self.fetchworker.start() # when action finished -> send finished signal


    def clear_fetch_results(self):
        while self.result_content_widget.layout().count():
            item = self.result_content_widget.layout().takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        try:
            self.fetch_errorLabel.deleteLater()
        except:
            pass

        self.scroll_area.hide()
        






    def on_received(self, data):
        # Clear the old results:
        self.clear_fetch_results()



        if data:
            # meta data item
            self.meta_data = QFrame()
            self.meta_data.setObjectName("card")

            self.meta_data_layout = QVBoxLayout(self.meta_data)

            self.video_title_data = QLabel(f"{data['metadata']['title']}")
            self.video_title_data.setWordWrap(True)
            self.video_title_data.setMaximumHeight(40)

            minutes = data['metadata']['duration'] // 60
            seconds = data['metadata']['duration'] % 60
            self.video_uploader_duration = QLabel(f"{data['metadata']['uploader']} . {minutes}:{seconds:02d} ")
            self.meta_data_layout.addWidget(self.video_title_data)
            self.meta_data_layout.addWidget(self.video_uploader_duration)



            self.result_content_widget.layout().addWidget(self.meta_data)
            self.result_content_widget.layout().addSpacing(20) 


            # the formats:
            self.formats = QFrame()

            self.formats_layout = QVBoxLayout(self.formats)
            for f in data['formats']:
                self.add_download_item(f['format_id'], f['ext'], f['resolution'])


            self.result_content_widget.layout().addWidget(self.formats)

            self.result_content_widget.layout().addStretch()

            self.scroll_area.show()

        else:
            # show try again label in the bottom of the url row
            self.fetch_errorLabel = QLabel("<b>Fetch Failed!</b> Check your URL and try again.")

            self.fetch_errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.fetch_errorLabel.setStyleSheet("color: #FF5252; padding: 25px; border-top: 1px solid #3a3a36;")
    
            self.result_content_widget.layout().addWidget(self.fetch_errorLabel)
            self.scroll_area.show()
            


        if self.url_lineedit.text() != "":
            self.clear_fetch_btn.show()

        self.fetch_btn.setText("Fetch") 
        self.fetch_btn.setDisabled(False)
        self.url_lineedit.setDisabled(False)



    def add_download_item(self, format_id, ext, resolution):
        item = QFrame()

        item.setObjectName("format_card")
        item.setProperty("type", "audio" if resolution == "Audio" else "video")

        item_layout = QVBoxLayout(item)

        format_label = QLabel(f"{format_id}")
        format_label.hide()

        exntension_label = QLabel(f"{ext}")
        exntension_label.setObjectName("card_details")


        resolution_label = QLabel(f"{resolution}")

        resolution_label.setObjectName("card_type_title")
        resolution_label.setProperty("type", "audio" if resolution == "Audio" else "video")


        downloadBtn = QPushButton(" Download")
        downloadBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        downloadBtn.setObjectName("card_download_btn")
        downloadBtn.setIcon(QIcon(r"utilityhub\assets\inactive_tab_btns\down_arrow.png"))
        downloadBtn.setIconSize(QSize(16, 16))

        downloadBtn.setProperty("type", "audio" if resolution == "Audio" else "video")

        is_audio_stream = (resolution == "Audio")
        downloadBtn.clicked.connect(lambda : self.start_downloadMedia(format_id, is_audio_stream))


        item_layout.addWidget(format_label)
        item_layout.addWidget(resolution_label)
        item_layout.addWidget(exntension_label)
        item_layout.addWidget(downloadBtn)

        self.formats_layout.addWidget(item)




    def start_downloadMedia(self, format_id, is_audio):
        self.result_content_widget.setDisabled(True)
        self.fetch_btn.setDisabled(True)
        self.url_lineedit.setDisabled(True)

        self.nbr_of_downloads += 1
        idI = self.nbr_of_downloads

        info = {
            "id": idI,
            "url":self.current_fetched_url,
            "format_id":format_id,
            "is_audio":is_audio
        }
        self.download_queue.append(info)

        # process the download (wait or start download)
        self.process_queue()

        self.add_queue_row(idI, self.video_title_data.text() )



        self.fetch_btn.setDisabled(False)
        self.url_lineedit.setDisabled(False)



    def process_queue(self):
        # check if downloading, no one waiting -> stop
        if self.is_currently_downloading or not self.download_queue:
            return 

        # else start downloading first one in Queue (FIFO):
        self.is_currently_downloading = True  # to stop other workers
        info = self.download_queue.pop(0)
        self.current_worker_id = info['id'] # save current worker to kill if op cancelled


        self.downloadworker = DownloadWorker(info['url'], info['format_id'], self.download_service, info['is_audio'])


        #  call on_received when the signal finished is sent
        self.downloadworker.finished.connect(lambda status, message, idI= info['id'] : self.on_received_finished_downloadMedia(status,message, idI)) 

        # progress signal to update progress:
        self.downloadworker.progress.connect(self.update_log_progress)

        self.downloadworker.start() # when action finished -> send finished signal




    def on_received_finished_downloadMedia(self, status_str, outfileName, idI):
        # that means the downloading now is finished
        try:
            self.is_currently_downloading = False

            print(f"finished Signal id#: {idI}")


            if status_str == "SUCCESS":
                self.log_console.setText(f"Download Finished Successfully!")
            else:
                self.log_console.setText(f"Operation Failed or Canceled.")
                self.delete_junck(outfileName)

                self.result_content_widget.setDisabled(False)
            status = self.queue_refs.get(idI)
            if status:
                status.setText("Done")
                status.setStyleSheet("background-color: #04342C; color: #2ECC71; border-radius: 12px; font-weight: bold; padding: 4px 35px 4px 12px;")

        

        except Exception as e:
            print(f"Receiver Error: {e}")

            
        # process the next download: (if available )
        self.process_queue()




    def update_log_progress(self, data):
        if data.get('status') == 'downloading':
            downloaded = data.get('downloaded_bytes', 0)
            total = data.get('total_bytes') or data.get('total_bytes_estimate', 0)
            speed = data.get('speed', 0)
            estimated_time = data.get('eta', 0)

            percent = ( downloaded / total * 100) if total > 0 else 0
            speed_mb = speed / (1024 * 1024) if speed else 0
            total_mib = total / (1024 * 1024)


            self.log_console.setText(
                f"{percent:.1f}% of {total_mib:.2f}MiB at {speed_mb:.2f}MiB/s ETA {estimated_time}s"
            )



class FetchWorker(QThread):
    finished = pyqtSignal(object)

    def __init__(self, url, service):
        super().__init__()
        self.url = url
        self.service = service



    def run(self):
        data = self.service.get_media_info(self.url)
        self.finished.emit(data) # when done send data




class DownloadWorker(QThread):
    """
    this is just waiting for the internet (I/O bound) so it doesn't block the UI. that's why this one feels smoother than the converter.
    """



    progress = pyqtSignal(dict) # {percentage, speed, ETA}
    finished = pyqtSignal(str, str) # {sucessStatus, error Or outputPath}

    """
    .terminate() crash the app because when the yt-dlp is killed
    and we try to download again it finds some remaining files 
    causing the app to crash

    we can't just delete them because .terminate dont let the yt-dlp release the file
    solution: soft_kill
    """

    def __init__(self, url, format_choice ,service, is_audio):
        super().__init__()
        self.url = url 
        self.format_choice = format_choice
        self.service = service
        self.is_audio = is_audio
        self.is_killed = False


    def run(self):
        status , outfileName = self.service.download_media(self.url, self.format_choice, self.hook, self.is_audio)
        self.finished.emit(status, outfileName) 



    def hook(self, yt_dlp_sent_data : dict):
        if self.is_killed:
            raise Exception("Download Canceled!")
        self.progress.emit(yt_dlp_sent_data)




