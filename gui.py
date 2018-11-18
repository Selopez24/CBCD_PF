# GUI
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import match_functions as match
import descdb as db 
import cv2
import numpy as np
from match_functions import get_candidates_id
from descdb import get_names
import time

# Load .ui file

form_class = uic.loadUiType("gui.ui")[0]

style = """QTabWidget::tab-bar{
    alignment: left;
    margin-right: 1000;
    margin-left: 1000;

    height: 80; 
    width: 20;
}"""


# Window Class
class MyWindowClass(QtWidgets.QTabWidget, QtWidgets.QGraphicsView ,form_class, QtGui.QPixmap):
    def __init__(self, parent=None):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.setupUi(self)
        self.load_btn1.clicked.connect(self.load_btn1_clicked)
        self.candidates_btn.clicked.connect(self.candidates_btn_clicked)
        self.setStyleSheet(style)
        self.options_btn.setIcon(QtGui.QIcon('../figures/options.png'))
        self.options_btn.clicked.connect(self.options_btn_clicked)
        # self.score_btn.clicked.connect(self.score_btn_clicked)
        self.basic_option.toggled.connect(self.basic_on)
        self.expert_option.toggled.connect(self.expert_on)
        self.basic_option.hide()
        self.expert_option.hide()

        #tab 2
        self.load_btn2.clicked.connect(self.load_btn2_clicked)
        self.load_btn3.clicked.connect(self.load_btn3_clicked)
        self.options_btn2.setIcon(QtGui.QIcon('../figures/options.png'))
        self.options_btn2.clicked.connect(self.options_btn2_clicked)
        # self.score_btn2.clicked.connect(self.score_btn_clicked2)
        self.basic_option2.toggled.connect(self.basic_on2)
        self.expert_option2.toggled.connect(self.expert_on2)
        self.basic_option2.hide()
        self.expert_option2.hide()

# Buttons events

    def load_btn1_clicked(self): # load files

        self.query_filename.clear()
        self.load_done.clear()


        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
        self.query_filename.append(str(fileName))

        bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=False)

        bf.clear()
        match.train_fromdb()
        
        fig_query = 'gui'
        fig_path = '../figures/fig_%s.png'



        match.spectrogram_gen(fileName, fig_query ) #query file // fig_id



        newfont = QtGui.QFont("Sans Serif", 18, QtGui.QFont.Bold) 



        self.load_done.setText('Succesfully loaded!')
        self.load_done.setStyleSheet('color: #703460')
        self.load_done.setFont(newfont)

        pixmap = QtGui.QPixmap(fig_path % (fig_query))

        self.img_label.setPixmap(pixmap)

        self.show()

        

    def candidates_btn_clicked(self): # get candidates

        self.candidates_list.clear()
        #self.search_done.clear()


        fig_query = 'gui'
        fig_path = '../figures/fig_%s.png'
        orb = cv2.ORB_create()

        
        img_q = cv2.imread(fig_path % (fig_query), cv2.IMREAD_GRAYSCALE) # image for kp and desc extratcion 
        kp_q, desc_q = orb.detectAndCompute(img_q, None) # kp and desc for query image/audio sample

        # Candidates output ====>



        candidates_id = match.get_candidates_id(desc_q)

        names = db.get_names(candidates_id)


        for name in names:
            self.candidates_list.addItem(name)
            print(name)


        newfont = QtGui.QFont("Sans Serif", 18, QtGui.QFont.Bold) 

        # self.search_done.setText('Candidates found')
        # self.search_done.setStyleSheet('color: #703460')
        # self.search_done.setFont(newfont)
        
    def options_btn_clicked(self):

        self.basic_option.show()
        self.expert_option.show()



    def basic_on(self):

        if self.basic_option.text() == "Basic":
            if self.basic_option.isChecked() == True:
                print (self.basic_option.text()+" is selected")
            else:
                print (self.basic_option.text()+" is deselected")


        time.sleep(0.1)

        self.basic_option.hide()
        self.expert_option.hide()

    def expert_on(self):

        if self.expert_option.text() == "Expert":
            if self.expert_option.isChecked() == True:
                print (self.expert_option.text()+" is selected")
            else:
                print (self.expert_option.text()+" is deselected")
       
        time.sleep(0.1)

        self.basic_option.hide()
        self.expert_option.hide()


# Tab 2 Widgets

    def load_btn2_clicked(self): # load files

            self.query_filename2.clear()
            self.load_done2.clear()


            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print(fileName)
            self.query_filename2.append(str(fileName))

            bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=False)

            bf.clear()
            match.train_fromdb()
            
            fig_query = 'gui'
            fig_path = '../figures/fig_%s.png'



            match.spectrogram_gen(fileName, fig_query ) #query file // fig_id



            newfont = QtGui.QFont("Sans Serif", 18, QtGui.QFont.Bold) 



            self.load_done2.setText('Succesfully loaded!')
            self.load_done2.setStyleSheet('color: #703460')
            self.load_done2.setFont(newfont)

            pixmap = QtGui.QPixmap(fig_path % (fig_query))

            self.img_label2.setPixmap(pixmap)

            self.show()

    def load_btn3_clicked(self): # load files

            self.query_filename3.clear()
            self.load_done3.clear()


            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print(fileName)
            self.query_filename3.append(str(fileName))

            bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=False)

            bf.clear()
            match.train_fromdb()
            
            fig_query = 'gui'
            fig_path = '../figures/fig_%s.png'



            match.spectrogram_gen(fileName, fig_query ) #query file // fig_id



            newfont = QtGui.QFont("Sans Serif", 18, QtGui.QFont.Bold) 



            self.load_done3.setText('Succesfully loaded!')
            self.load_done3.setStyleSheet('color: #703460')
            self.load_done3.setFont(newfont)

            pixmap = QtGui.QPixmap(fig_path % (fig_query))

            self.img_label3.setPixmap(pixmap)

            self.show()

    def options_btn2_clicked(self):

            self.basic_option2.show()
            self.expert_option2.show()

    def basic_on2(self):

        if self.basic_option2.text() == "Basic":
            if self.basic_option2.isChecked() == True:
                print (self.basic_option2.text()+" is selected")
            else:
                print (self.basic_option2.text()+" is deselected")


        time.sleep(0.1)

        self.basic_option2.hide()
        self.expert_option2.hide()

    def expert_on2(self):

        if self.expert_optio2n.text() == "Expert":
            if self.expert_option2.isChecked() == True:
                print (self.expert_option2.text()+" is selected")
            else:
                print (self.expert_option2.text()+" is deselected")
    
        time.sleep(0.1)

        self.basic_option2.hide()
        self.expert_option2.hide()



app = QtWidgets.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()