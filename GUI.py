# -*- coding: utf-8 -*-

# import
import sys
from PyQt5.QtCore import qFatal, Qt, QTimer
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsView,\
    QGraphicsScene
import Controller


# errors management
import traceback


def excepthook(type_, value, traceback_):
    traceback.print_exception(type_, value, traceback_)
    qFatal('')


sys.excepthook = excepthook

# class


class mainWindow(QMainWindow):
    def __init__(self, generationNumber, specie, app):
        super().__init__()
        self.setWindowTitle("Window")
        self.timer = QTimer()
        self.controller = Controller.Controller(generationNumber, specie)
        self.centralWidget = GraphicView(self, self.timer, self.controller,
                                         app)
        self.setCentralWidget(self.centralWidget)


class GraphicView(QGraphicsView):
    def __init__(self, parent, timer, controller, app):
        super().__init__(parent)
        self.mainScene = GraphicScene(self, timer, controller, app)
        self.setScene(self.mainScene)


class GraphicScene(QGraphicsScene):
    def __init__(self, parent, timer, controller, app):
        super().__init__(parent)
        self.c = controller
        self.c.add(self)
        self.timer = timer
        self.setSceneRect(*self.c.WINDOW_SIZE)
        self.eog = False
        self.app = app

        for cage in self.c.getCageList():
            pen = QPen(QColor(0, 0, 0), 1, Qt.DotLine)
            brush = QBrush(QColor(*cage.color), Qt.SolidPattern)
            self.addRect(*cage.upRightCorner, cage.w, cage.h, pen, brush)

        self.dictEllipse = {}
        for player in self.c.getPlayerList():
            playerX, playerY, playerSize, playerColor = \
                self.c.getPlayerInformations(player)
            pen = QPen(QColor(*playerColor), 1, Qt.SolidLine)
            brush = QBrush(QColor(*playerColor), Qt.SolidPattern)
            self.dictEllipse[player] = (self.addEllipse(0, 0, playerSize,
                                                        playerSize, pen,
                                                        brush))

        self.c.refresh()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(self.c.game.gameTick)

    def updateTimer(self):
        self.c.refresh()

    def keyPressEvent(self, event):
        if not self.c.isAI(0) or not self.c.isGOAL(0):
            if event.key() == Qt.Key_Up:
                self.c.saveData(self.c.JUMP)
                self.c.movePlayer(self.c.JUMP, 0)
                self.c.refresh()

            if event.key() == Qt.Key_Left:
                self.c.saveData(self.c.LEFT)
                self.c.movePlayer(self.c.LEFT, 0)
                self.c.refresh()

            if event.key() == Qt.Key_Right:
                self.c.saveData(self.c.RIGHT)
                self.c.movePlayer(self.c.RIGHT, 0)
                self.c.refresh()

        if not self.c.isAI(1) or not self.c.isGOAL(1):
            if event.key() == Qt.Key_Z:
                self.c.saveData(self.c.JUMP)
                self.c.movePlayer(self.c.JUMP, 1)
                self.c.refresh()

            if event.key() == Qt.Key_Q:
                self.c.saveData(self.c.LEFT)
                self.c.movePlayer(self.c.LEFT, 1)
                self.c.refresh()

            if event.key() == Qt.Key_D:
                self.c.saveData(self.c.RIGHT)
                self.c.movePlayer(self.c.RIGHT, 1)
                self.c.refresh()

    def refresh(self):
        self.c.moveAI()
        self.c.placeGoal()
        self.c.collisions()
        for player in self.c.getPlayerList():
            playerX, playerY = self.c.getPlayerPosition(player)
            self.dictEllipse[player].setPos(playerX, playerY)
        self.c.updateTime()
        self.eog = self.c.checkEndOfGame()
        if self.eog:
            self.app.quit()

# launch the GUI


def main(generation, specie):
    app = QApplication(sys.argv)
    window = mainWindow(generation, specie, app)
    window.show()
    app.exec()


if __name__ == '__main__':
    main(0, 0)
