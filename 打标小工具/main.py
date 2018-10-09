# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from Ui_patch_label import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import sys,os

#config
FILE_LIST = []
STATE = None
SAVE_PATH = None
LABEL_PATH = None


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        #选取标图
        #label_url, type = QFileDialog.getOpenFileName(self,'选取文件','./','All Files (*);;Image Files (*.png,*.jpg,*.jpeg)')
        label_url, type = QFileDialog.getOpenFileName(self,'选取文件','./')
        if label_url:
            self.label.setPixmap(QtGui.QPixmap(label_url))
            self.label.setScaledContents(True)
            global LABEL_PATH
            LABEL_PATH = label_url

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        #选取被打标图
        file_path_obj, type = QFileDialog.getOpenFileUrls(self,'选取文件','./')
        if file_path_obj:
            raw_file_path = [ file.path()[1:] for file in file_path_obj ]
            pic_type = ['jpg','gif','jpeg','tiff','svg','png','ico']
            global FILE_LIST
            FILE_LIST = []
            file_list_tmp = []
            for file in raw_file_path:
                if os.path.isfile(file):
                    f_s = file.split('.')
                    if len(f_s) >= 2:
                        suffix = f_s[-1].lower()
                        if suffix in pic_type:
                            file_list_tmp.append(file)
            if len(file_list_tmp) > 0:
                self.textBrowser.setText('')
                # self.textBrowser.acceptDrops()
                # self.textBrowser.close()
                # self.textBrowser.clearMask()
            for f_name in file_list_tmp:
                self.textBrowser.append(f_name)
            FILE_LIST = file_list_tmp

    @pyqtSlot()
    def on_pushButton_3_clicked(self):

        #开始打标
        num = self.whichchecked()
        x = self.lineEdit.text()
        y = self.lineEdit_2.text()
        if not x.isdigit() or  not y.isdigit():
            QMessageBox.warning(self,'坐标有问题','1111')
            return
        else:
            x = int(x)
            y = int(y)
        if not FILE_LIST or not SAVE_PATH or not LABEL_PATH:
            QMessageBox.warning(self,'坐标有问题','1111')
            return
        print(FILE_LIST,SAVE_PATH,LABEL_PATH)
        self.pushButton_3.setText('打标中...')
        self.thread = Runthread(LABEL_PATH, num, FILE_LIST, (x,y), SAVE_PATH)
        self.thread._signal.connect(self.recover)
        self.thread.start()
        #finish, fail_list = merge_label(LABEL_PATH, num, FILE_LIST, (x,y), SAVE_PATH)

    def recover(self):
        self.pushButton_3.setText('开始打标')

    def whichchecked(self):
        if self.checkBox.checkState():
            return 1
        if self.checkBox_2.checkState():
            return 2
        if self.checkBox_3.checkState():
            return 3
        if self.checkBox_4.checkState():
            return 4

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        #保存路径
        path = QFileDialog.getExistingDirectory(self,'选取文件夹','./')
        if path:
            global SAVE_PATH
            SAVE_PATH = path
            self.textBrowser_2.setText(path)

    @pyqtSlot('bool')
    def on_checkBox_clicked(self,checked):
        if checked:
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)

    @pyqtSlot('bool')
    def on_checkBox_2_clicked(self,checked):
        if checked:
            self.checkBox.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)

    @pyqtSlot('bool')
    def on_checkBox_3_clicked(self,checked):
        if checked:
            self.checkBox_2.setChecked(False)
            self.checkBox.setChecked(False)
            self.checkBox_4.setChecked(False)

    @pyqtSlot('bool')
    def on_checkBox_4_clicked(self,checked):
        if checked:
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox.setChecked(False)

class Runthread(QtCore.QThread):
    _signal = pyqtSignal(bool)

    def __init__(self, label_path, num, file_list, pic_pos, save_path, parent=None,):
        super(Runthread, self).__init__()
        self.label_path = label_path
        self.num = num
        self.file_list = file_list
        self.pic_pos = pic_pos
        self.save_path = save_path

    def __del__(self):
        self.wait()

    def run(self):
        from batch_label import merge_label
        finish, fail_list = merge_label(self.label_path, self.num, self.file_list, self.pic_pos, self.save_path)
        self._signal.emit(finish)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())



