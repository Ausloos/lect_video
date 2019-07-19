import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_lecteur_video import Ui_MainWindow
from PySide2.QtCore import QUrl, QTime
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pblecture.clicked.connect(self.lectureClicked)
        self.ui.pbpause.clicked.connect(self.pauseClicked)
        self.ui.pbstop.clicked.connect(self.stopClicked)

        self.ui.pbmoins.clicked.connect(self.moinsClicked)
        self.ui.pbplus.clicked.connect(self.plusClicked)

        self.mediaPlayer = QMediaPlayer() #creation de la variable mediaPlayer
        self.mediaPlayer.setVideoOutput(self.ui.ecran) #on projette la var mediaPlayer sur ecran.

        self.ui.dialVolume.valueChanged.connect(self.volumeChanged)
        #self.ui.dialVolume.valueChanged.connect(self.ui.lcdVol.display)

        self.mediaPlayer.durationChanged.connect(self.mediaDurationChanged)
        self.mediaPlayer.positionChanged.connect(self.mediaPositionChanged)

     #   self.ui.timeline.valueChanged.connect(self.slideChanged)

        # Commande qui permet de lancer le film (depuis le début)
        mediaContent = QMediaContent(QUrl.fromLocalFile("big_buck_bunny.avi"))
        self.mediaPlayer.setMedia(mediaContent)

    #def slideChanged(self):
    #    self.mediaPlayer.position()
    #    self.ui.timeline.setValue()

    def mediaDurationChanged(self):
        self.ui.debut.setText("00:00:00")
        mediaDuration = self.mediaPlayer.duration() #recoit le temps total en Millisec
        self.ui.timeline.setRange(0, mediaDuration) #découpe le timeline proportionnelement au temps en millisec
        totalTimeMedia = QTime(0, 0, 0)
        totalTimeMedia = totalTimeMedia.addMSecs(mediaDuration) #convertit le temps total en h:m:s
        self.ui.fin.setText(totalTimeMedia.toString("HH:mm:ss"))

    def mediaPositionChanged(self):
        mediaPosition = self.mediaPlayer.position()
        self.ui.timeline.setValue(mediaPosition)
        currentTimeMedia = QTime(0, 0, 0,)
        currentTimeMedia = currentTimeMedia.addMSecs(mediaPosition)
        self.ui.debut.setText(currentTimeMedia.toString("HH:mm:ss"))

    def volumeChanged(self):
        self.mediaPlayer.setVolume(self.ui.dialVolume.value())
        self.ui.labelVol.setText(str(self.ui.dialVolume.value())+"%")

    def lectureClicked(self):
        print("Lecture!!")
        self.mediaPlayer.play()

    def pauseClicked(self):
        print("Pause !!")
        if self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.mediaPlayer.play()
        elif self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

    def stopClicked(self):
        print("Stop!!")
        self.mediaPlayer.stop()

    def moinsClicked(self):
        print("Enlève un fichier")
    def plusClicked(self):
        print("Ajoute un fichier")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())