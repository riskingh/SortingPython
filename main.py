#!/usr/bin/python3

from PySide import QtGui, QtCore
import sys

import folder_dfs, os

class MainWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(640, 480)
        self.setWindowTitle("SortingPython")

        self.mainLayout = QtGui.QVBoxLayout(self)

        #chooseMainFolder*
        self.chooseMainFolderButton = QtGui.QPushButton("Choose main folder")
        self.chooseMainFolderDialog = QtGui.QFileDialog(self, "Main folder")
        self.chooseMainFolderDialog.setFileMode(QtGui.QFileDialog.Directory)
        self.chooseMainFolderDialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        self.chooseMainFolderLineEdit = QtGui.QLineEdit()

        self.chooseMainFolderLayout = QtGui.QHBoxLayout()
        self.chooseMainFolderLayout.addWidget(self.chooseMainFolderButton)
        self.chooseMainFolderLayout.addWidget(self.chooseMainFolderLineEdit)
        self.mainLayout.addLayout(self.chooseMainFolderLayout)

        QtCore.QObject.connect(self.chooseMainFolderButton, QtCore.SIGNAL("clicked()"), self.chooseMainFolderDialog, QtCore.SLOT("show()"))
        QtCore.QObject.connect(self.chooseMainFolderDialog, QtCore.SIGNAL("accepted()"), self, QtCore.SLOT("updateChooseMainFolderLineEdit()"))
        #end

        #chooseTemporaryFolder
        self.chooseTemporaryFolderButton = QtGui.QPushButton("Choose temporary folder")
        self.chooseTemporaryFolderDialog = QtGui.QFileDialog(self, "Temporary folder")
        self.chooseTemporaryFolderDialog.setFileMode(QtGui.QFileDialog.Directory)
        self.chooseTemporaryFolderDialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        self.chooseTemporaryFolderLineEdit = QtGui.QLineEdit()

        self.chooseTemporaryFolderLayout = QtGui.QHBoxLayout()
        self.chooseTemporaryFolderLayout.addWidget(self.chooseTemporaryFolderButton)
        self.chooseTemporaryFolderLayout.addWidget(self.chooseTemporaryFolderLineEdit)
        self.mainLayout.addLayout(self.chooseTemporaryFolderLayout)

        QtCore.QObject.connect(self.chooseTemporaryFolderButton, QtCore.SIGNAL("clicked()"), self.chooseTemporaryFolderDialog, QtCore.SLOT("show()"))
        QtCore.QObject.connect(self.chooseTemporaryFolderDialog, QtCore.SIGNAL("accepted()"), self, QtCore.SLOT("updateChooseTemporaryFolderLineEdit()"))
        #end

        #textEdit for contact to user
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setMinimumHeight(300)
        self.textEdit.setMaximumHeight(300)
        #self.textEdit.setEnabled(False)
        self.mainLayout.addWidget(self.textEdit)
        #end

        #buttons to interact
        self.infoButton = QtGui.QPushButton("info")
        self.infoButton.setMinimumWidth(100)
        self.infoButton.setMaximumWidth(100)

        self.sortButton = QtGui.QPushButton("sort")
        self.sortButton.setMinimumWidth(100)
        self.sortButton.setMaximumWidth(100)

        self.exitButton = QtGui.QPushButton("exit")
        self.exitButton.setMinimumWidth(100)
        self.exitButton.setMaximumWidth(100)

        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.addWidget(self.infoButton)
        self.buttonsLayout.addWidget(self.sortButton)
        self.buttonsLayout.addWidget(self.exitButton)
        self.mainLayout.addLayout(self.buttonsLayout)

        QtCore.QObject.connect(self.infoButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("infoButtonClicked()"))
        QtCore.QObject.connect(self.sortButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("sortButtonClicked()"))
        QtCore.QObject.connect(self.exitButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("exitButtonClicked()"))
        #end

    @QtCore.Slot()
    def updateChooseMainFolderLineEdit(self):
        self.chooseMainFolderLineEdit.setText(self.chooseMainFolderDialog.selectedFiles()[0])

    @QtCore.Slot()
    def updateChooseTemporaryFolderLineEdit(self):
        self.chooseTemporaryFolderLineEdit.setText(self.chooseTemporaryFolderDialog.selectedFiles()[0])

    def isDirectoriesAreCorrect(self):
        mainDir = self.chooseMainFolderLineEdit.text()
        tempDir = self.chooseTemporaryFolderLineEdit.text()
        return mainDir != "" and tempDir != "" and os.path.isdir(mainDir) and os.path.isdir(tempDir) and mainDir != tempDir

    def printToTextEdit(self, s):
        self.textEdit.setHtml(s)

    @QtCore.Slot()
    def infoButtonClicked(self):
        if not self.isDirectoriesAreCorrect():
            self.printToTextEdit("Wrong main directory")
        else:
            info = folder_dfs.fileTypes(self.chooseMainFolderLineEdit.text())
            self.printToTextEdit(str(info))
    
    @QtCore.Slot()
    def sortButtonClicked(self):
        if not self.isDirectoriesAreCorrect():
            self.printToTextEdit("Wrong main/temporary directory")
            return
        else:
            mainDir = self.chooseMainFolderLineEdit.text()
            tempDir = self.chooseTemporaryFolderLineEdit.text()
            folder_dfs.clearDir(tempDir)
            folder_dfs.unpack(mainDir, tempDir)
            folder_dfs.sortByType(tempDir)
            folder_dfs.sortFiles(tempDir)
            self.printToTextEdit("Done")

    @QtCore.Slot()
    def exitButtonClicked(self):
        self.close()

    


app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
