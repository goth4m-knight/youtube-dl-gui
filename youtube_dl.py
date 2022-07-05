import threading
from pytube import YouTube
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import urllib.request

downloading = []
downloaded = []


class CandyYTD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 900, 700
        self.setGeometry(450, 50, self.window_width, self.window_height)
        self.setMaximumWidth(self.window_width)
        self.setMaximumHeight(self.window_height)
        self.setWindowTitle("Candy Youtube Video Downloader")
        self.setWindowIcon(QIcon("candy-ytd-icon.ico"))
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.downloading = []
        self.downloaded = []

        # Layouts
        self.layout = QVBoxLayout(self.centralwidget)
        urlLayout = QHBoxLayout(self.centralwidget)
        infoboxLayout = QHBoxLayout(self.centralwidget)
        infobox = QVBoxLayout()
        subinfobox = QHBoxLayout()

        # Widgets
        self.title = QLabel()
        self.title.setText('Youtube Video Downloader')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Sitka Text', 11))

        self.urlEntry = QLineEdit()
        self.urlEntry.setFont(QFont('Sitka Text', 11))

        self.urlLabel = QLabel()
        self.urlLabel.setText("Video Url: ")
        self.urlLabel.setFont(QFont('Sitka Text', 11))

        self.searchBtn = QPushButton()
        self.searchBtn.setText('Search')
        self.searchBtn.clicked.connect(self.get_the_info)
        self.searchBtn.setFont(QFont('Sitka Text', 11))

        self.resolutionLabel = QLabel()
        self.resolutionLabel.setText("Resolution: ")
        self.resolutionLabel.setFont(QFont('Sitka Text', 11))

        self.resolutionCombobox = QComboBox()
        self.resolutionCombobox.setFixedWidth(150)
        self.resolutionCombobox.setFont(QFont('Sitka Text', 10))

        self.nameLabel = QLabel()
        self.nameLabel.setText("[Video Title]")
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setFont(QFont('Sitka Text', 15))

        self.downloadBtn = QPushButton()
        self.downloadBtn.setText('Download')
        self.downloadBtn.clicked.connect(self.download)
        self.downloadBtn.setFont(QFont('Sitka Text', 11))
        self.downloadBtn.setEnabled(False)

        self.showBtn = QPushButton()
        self.showBtn.setText('Show Downloads')
        self.showBtn.setFont(QFont('Sitka Text', 11))
        self.showBtn.clicked.connect(self.show_downloads)

        self.frame = QFrame()
        self.frame.setFixedSize(700, 550)

        self.thumbnailLabel = QLabel(self.frame)
        self.thumbnailLabel.setText("")
        self.thumbnailLabel.setAlignment(Qt.AlignRight)
        self.thumbnailLabel.setFixedSize(700, 550)

        # Adding Widgets
        urlLayout.addWidget(self.urlLabel)
        urlLayout.addWidget(self.urlEntry)
        urlLayout.addWidget(self.searchBtn)
        subinfobox.addWidget(self.resolutionLabel)
        subinfobox.addWidget(self.resolutionCombobox)
        infobox.addLayout(subinfobox)
        infobox.addWidget(self.downloadBtn)
        infobox.addWidget(self.showBtn)
        infoboxLayout.addLayout(infobox)
        infoboxLayout.addWidget(self.frame)
        self.layout.addWidget(self.title)
        self.layout.addLayout(urlLayout)
        self.layout.addWidget(self.nameLabel)
        self.layout.addLayout(infoboxLayout)

    def get_the_info(self):
        def info():
            try:
                resolutions = []
                yt = YouTube(self.urlEntry.text())
                self.setWindowTitle(f'Candy YTD - {yt.title}')
                for stream in yt.streams.filter(progressive=True):
                    resolutions.append(stream.resolution)

                self.nameLabel.setText(f"{yt.title}")

                for resolution in resolutions:
                    self.resolutionCombobox.addItem(resolution)

                data = urllib.request.urlopen(yt.thumbnail_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.thumbnailLabel.setPixmap(pixmap)
                self.downloadBtn.setEnabled(True)
            except Exception as e:
                self.setWindowTitle(f'Candy YTD - Search Error! {e}')
                pass
        
        threading.Thread(target=info).start()

    def download(self):
        def download():
            try:
                yt = YouTube(self.urlEntry.text())
                downloading.append(yt.title)
                if len(downloading) == 1:
                    self.setWindowTitle(f'Candy YTD - Downloading {yt.title}')
                else:
                    self.setWindowTitle(f'Candy YTD - Downloading {len(downloading)} files')
                stream = yt.streams.get_by_resolution(self.resolutionCombobox.currentText())
                stream.download(output_path='C:/Users/%s/Videos' % os.getlogin())
                downloading.remove(yt.title)
                downloaded.append(yt.title)
                self.setWindowTitle(f'Candy YTD - Downloaded {yt.title}')
                self.downloadBtn.setEnabled(False)
            except Exception as e:
                self.setWindowTitle(f'Candy YTD - Download Error! {e}')
                pass

        self.t = threading.Thread(target=download)
        self.t.start()

    def show_downloads(self):
        popup = Popup(self)
        popup.show()

    def closeEvent(self, event):
        if threading.Thread.is_alive(self.t):
            close = QMessageBox.question(self, "QUIT", "Downloading still in progress. Are you sure you want to quit?",
                                         QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
                exit()
            else:
                event.ignore()


class Popup(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Downloads')
        self.resize(900, 400)
        self.list = QListWidget(self)
        self.list.setGeometry(0, 0, 900, 400)
        x = 0
        for files in downloading:
            self.list.insertItem(x, f'{files} - Downloading')
            self.list.setFont(QFont('Sitka Text', 11))
            x += 1
        for file in downloaded:
            self.list.insertItem(x, f'{file} - Downloaded')
            self.list.setFont(QFont('Sitka Text', 11))
            x += 1

        self.list.clicked.connect(self.open_folder)

    def open_folder(self):
        os.startfile(f'C:/Users/{os.getlogin()}/Videos')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    CandyYTD = CandyYTD()
    CandyYTD.show()
    sys.exit(app.exec_())
