import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from ui_lecteur_video import Ui_MainWindow
from PySide2.QtCore import QUrl, QTime, QFileInfo
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pblecture.clicked.connect(self.lectureClicked)
        self.ui.pbpause.clicked.connect(self.pauseClicked)
        self.ui.pbstop.clicked.connect(self.stopClicked)
        self.ui.pbmoins.clicked.connect(self.supprMedia)
        self.ui.pbplus.clicked.connect(self.ajouterMedia)
        self.ui.pbprecedent.clicked.connect(self.precedentClicked)
        self.ui.pbsuivant.clicked.connect(self.suivantClicked)
        self.mediaPlayer = QMediaPlayer() #creation de la variable mediaPlayer
        self.mediaPlayer.setVideoOutput(self.ui.ecran) #on projette la var mediaPlayer sur ecran.
        self.ui.dialVolume.valueChanged.connect(self.volumeChanged)
        self.mediaPlayer.durationChanged.connect(self.mediaDurationChanged)
        self.mediaPlayer.positionChanged.connect(self.mediaPositionChanged)
        self.ui.listWidget.itemDoubleClicked.connect(self.mediaSelected)

        # Commande qui permet de lancer le film (depuis le début)
        mediaContent = QMediaContent(QUrl.fromLocalFile("big_buck_bunny.avi"))
        self.mediaPlayer.setMedia(mediaContent)

    #def slideChanged(self):
    #    self.mediaPlayer.position()
    #    self.ui.timeline.setValue()
    def ajouterMedia(self):
        nomMedia = QFileDialog.getOpenFileName(self,"ChoixFilm", "c:/Users/AELION/PycharmProjects/lect_video", "(*.avi *.mp4)")
        fInfo = QFileInfo(nomMedia[0])
        fShortName = fInfo.baseName()
        item = QListWidgetItem(fShortName)
        item.setToolTip(nomMedia[0])
        self.ui.listWidget.addItem(item)

    def suivantClicked(self):
        currentItemRow = self.ui.listWidget.currentRow()
        if currentItemRow == -1:
            return
        totalItems = self.ui.listWidget.count()
        self.ui.listWidget.setCurrentRow((currentItemRow+1)%totalItems)
        self.mediaSelected()

    def precedentClicked(self):
        currentItemRow = self.ui.listWidget.currentRow()
        if currentItemRow == -1:
            return
        totalItems = self.ui.listWidget.count()
        self.ui.listWidget.setCurrentRow((currentItemRow - 1) % totalItems)
        self.mediaSelected()

    def supprMedia(self):
        rowItem = self.ui.listWidget.currentRow()
        if rowItem != -1:  #au cas ou on appuie sur Supp et qu'il n'y a pas d'objet
            self.ui.listWidget.takeItem(rowItem)

    def mediaSelected(self):
        currentItem = self.ui.listWidget.currentItem()
        mediaContent = QMediaContent(QUrl.fromLocalFile(currentItem.toolTip()))
        self.mediaPlayer.setMedia(mediaContent)
        self.lectureClicked()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())