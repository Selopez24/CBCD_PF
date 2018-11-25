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
import features 
import score
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
class MyWindowClass(QtWidgets.QTabWidget, QtWidgets.QGraphicsView ,form_class, QtGui.QPixmap, QtWidgets.QScrollArea):
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
        self.candidates_list.itemActivated.connect(self.change_plot)


        #tab 2
        self.load_btn2.clicked.connect(self.load_btn2_clicked)
        self.load_btn3.clicked.connect(self.load_btn3_clicked)
        self.options_btn2.setIcon(QtGui.QIcon('../figures/options.png'))
        self.options_btn2.clicked.connect(self.options_btn2_clicked)
        self.score_btn2.clicked.connect(self.score_btn2_clicked)
        self.basic_option2.toggled.connect(self.basic_on2)
        self.expert_option2.toggled.connect(self.expert_on2)
        self.basic_option2.hide()
        self.expert_option2.hide()

# Buttons events

    def load_btn1_clicked(self): # load files

        self.query_filename.clear()
        self.load_done.clear()
        self.img_label.clear()

        global fileName

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
        fig_read = 'mel'



        match.spectrogram_gen(fileName, fig_query ) #query file // fig_id

        features.MelSpectogram(fileName)
        #features.PitchRange(fileName)


        newfont = QtGui.QFont("Sans Serif", 28, QtGui.QFont.Bold) 
        newfont2 = QtGui.QFont("Sans Serif", 18) 



        self.load_done.setText('Succesfully loaded!')
        self.load_done.setStyleSheet('color: #32936F')
        self.load_done.setFont(newfont)

        self.fig_title3.setText('Mel Power Spectrogram')
        self.fig_title3.setStyleSheet('color: #000000')
        self.fig_title3.setFont(newfont2)

        self.fig_sub3.setText('%s' % (fileName))
        self.fig_sub3.setStyleSheet('color: #000000')
        self.fig_sub3.setFont(newfont2)

        pixmap = QtGui.QPixmap(fig_path % (fig_read))

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


        #newfont = QtGui.QFont("Sans Serif", 28, QtGui.QFont.Bold) 

        # self.search_done.setText('Candidates found')
        # self.search_done.setStyleSheet('color: #32936F')
        # self.search_done.setFont(newfont)
        
    def options_btn_clicked(self):

        self.basic_option.show()
        self.expert_option.show()

    def options_btn2_clicked(self):

        self.basic_option2.show()
        self.expert_option2.show()


    def basic_on(self):


        features.MelSpectogram_db(candidate_text)

        fig_path = '../figures/fig_%s.png'
        fig_read = 'mel'

        newfont = QtGui.QFont("Sans Serif", 18) 

        self.fig_title4.setText('Mel Power Spectrogram')
        self.fig_title4.setStyleSheet('color: #000000')
        self.fig_title4.setFont(newfont)

        self.fig_sub4.setText('%s' % (candidate_text))
        self.fig_sub4.setStyleSheet('color: #000000')
        self.fig_sub4.setFont(newfont)

        pixmap = QtGui.QPixmap(fig_path % (fig_read))

        self.img_label4.setPixmap(pixmap)

        self.show()

        print(candidate_text)




        self.basic_option.hide()
        self.expert_option.hide()

    def basic_on2(self):


        features.MelSpectogram_db(fileName3)

        fig_path = '../figures/fig_%s.png'
        fig_read = 'mel'

        newfont = QtGui.QFont("Sans Serif", 18) 

        self.fig_title3_2.setText('Mel Power Spectrogram')
        self.fig_title3_2.setStyleSheet('color: #000000')
        self.fig_title3_2.setFont(newfont)

        self.fig_sub3_2.setText('%s' % (fileName3))
        self.fig_sub3_2.setStyleSheet('color: #000000')
        self.fig_sub3_2.setFont(newfont)

        pixmap = QtGui.QPixmap(fig_path % (fig_read))

        self.img_label3.setPixmap(pixmap)

        self.show()

        print(candidate_text)




        self.basic_option.hide()
        self.expert_option.hide()

    def expert_on(self):




        features.PitchRange_db(candidate_text)

        fig_path = '../figures/fig_%s.png'
        fig_read = 'pitch'

        newfont = QtGui.QFont("Sans Serif", 18) 

        self.fig_title4.setText('Pitch range using ACF')
        self.fig_title4.setStyleSheet('color: #000000')
        self.fig_title4.setFont(newfont)

        self.fig_sub4.setText('%s' % (candidate_text))
        self.fig_sub4.setStyleSheet('color: #000000')
        self.fig_sub4.setFont(newfont)

        pixmap = QtGui.QPixmap(fig_path % (fig_read))

        self.img_label4.setPixmap(pixmap)

        self.show()

        features.PitchRange(fileName)

        fig_path = '../figures/fig_%s.png'
        fig_read = 'pitch'

        newfont = QtGui.QFont("Sans Serif", 18) 

        self.fig_title3.setText('Pitch range using ACF')
        self.fig_title3.setStyleSheet('color: #000000')
        self.fig_title3.setFont(newfont)

        self.fig_sub3.setText('%s' % (fileName))
        self.fig_sub3.setStyleSheet('color: #000000')
        self.fig_sub3.setFont(newfont)

        pixmap = QtGui.QPixmap(fig_path % (fig_read))

        self.img_label.setPixmap(pixmap)

        self.show()

       

        self.basic_option.hide()
        self.expert_option.hide()

# List event

    def change_plot(self, item):

        global  candidate_text
        
        candidate_text = item.text()

        print(candidate_text)

        features.MelSpectogram_db(candidate_text)
        #features.PitchRange_db(candidate_text)

        fig_path = '../figures/fig_%s.png'
        fig_read = 'mel'

        newfont = QtGui.QFont("Sans Serif", 18) 

        self.fig_title4.setText('Mel Power Spectrogram')
        self.fig_title4.setStyleSheet('color: #000000')
        self.fig_title4.setFont(newfont)

        self.fig_sub4.setText('%s' % (candidate_text))
        self.fig_sub4.setStyleSheet('color: #000000')
        self.fig_sub4.setFont(newfont)

        pixmap = QtGui.QPixmap(fig_path % (fig_read))

        self.img_label4.setPixmap(pixmap)

        self.show()

        return candidate_text


# Tab 2 Widgets

    def load_btn2_clicked(self): # load files

        self.query_filename2.clear()
        self.load_done2.clear()
        self.img_label2.clear()

        global fileName2

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName2, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName2:
            print(fileName2)
        self.query_filename2.append(str(fileName2))

        bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=False)

        bf.clear()
        match.train_fromdb()
        
        fig_query = 'gui'
        fig_path = '../figures/fig_%s.png'
        fig_read = 'mel'



        match.spectrogram_gen(fileName2, fig_query ) #query file // fig_id

        features.MelSpectogram(fileName2)
        #features.PitchRange(fileName)


        newfont = QtGui.QFont("Sans Serif", 28, QtGui.QFont.Bold) 
        newfont2 = QtGui.QFont("Sans Serif", 18) 



        self.load_done2.setText('Succesfully loaded!')
        self.load_done2.setStyleSheet('color: #32936F')
        self.load_done2.setFont(newfont)

        self.fig_title2.setText('Mel Power Spectrogram')
        self.fig_title2.setStyleSheet('color: #000000')
        self.fig_title2.setFont(newfont2)

        self.fig_sub2.setText('%s' % (fileName2))
        self.fig_sub2.setStyleSheet('color: #000000')
        self.fig_sub2.setFont(newfont2)

        pixmap = QtGui.QPixmap(fig_path % (fig_read))

        self.img_label2.setPixmap(pixmap)


        self.show()

    def load_btn3_clicked(self): # load files

        self.query_filename3.clear()
        self.load_done3.clear()
        self.img_label3.clear()

        global fileName3

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName3, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName3:
            print(fileName3)
        self.query_filename3.append(str(fileName3))

        bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=False)

        bf.clear()
        match.train_fromdb()
        
        fig_query = 'gui'
        fig_path = '../figures/fig_%s.png'
        fig_read = 'mel'



        match.spectrogram_gen(fileName3, fig_query ) #query file // fig_id

        features.MelSpectogram(fileName3)
        #features.PitchRange(fileName)


        newfont = QtGui.QFont("Sans Serif", 28, QtGui.QFont.Bold) 
        newfont2 = QtGui.QFont("Sans Serif", 18) 



        self.load_done3.setText('Succesfully loaded!')
        self.load_done3.setStyleSheet('color: #32936F')
        self.load_done3.setFont(newfont)

        self.fig_title3_2.setText('Mel Power Spectrogram')
        self.fig_title3_2.setStyleSheet('color: #000000')
        self.fig_title3_2.setFont(newfont2)

        self.fig_sub3_2.setText('%s' % (fileName3))
        self.fig_sub3_2.setStyleSheet('color: #000000')
        self.fig_sub3_2.setFont(newfont2)

        pixmap = QtGui.QPixmap(fig_path % (fig_read))

        self.img_label3.setPixmap(pixmap)


        self.show()

    def expert_on2(self):

        features.PitchRange_db(fileName2)

        fig_path = '../figures/fig_%s.png'
        fig_read = 'pitch'

        newfont = QtGui.QFont("Sans Serif", 18) 

        self.fig_title2.setText('Pitch range using ACF')
        self.fig_title2.setStyleSheet('color: #000000')
        self.fig_title2.setFont(newfont)

        self.fig_sub2.setText('%s' % (fileName))
        self.fig_sub2.setStyleSheet('color: #000000')
        self.fig_sub2.setFont(newfont)

        pixmap = QtGui.QPixmap(fig_path % (fig_read))

        self.img_label2.setPixmap(pixmap)

        self.show()

        features.PitchRange(fileName3)

        fig_path = '../figures/fig_%s.png'
        fig_read = 'pitch'

        newfont = QtGui.QFont("Sans Serif", 18) 

        self.fig_title3_2.setText('Pitch range using ACF')
        self.fig_title3_2.setStyleSheet('color: #000000')
        self.fig_title3_2.setFont(newfont)

        self.fig_sub3_2.setText('%s' % (fileName))
        self.fig_sub3_2.setStyleSheet('color: #000000')
        self.fig_sub3_2.setFont(newfont)

        pixmap = QtGui.QPixmap(fig_path % (fig_read))

        self.img_label3.setPixmap(pixmap)

        self.show()

       


        self.basic_option2.hide()
        self.expert_option2.hide()

    def score_btn2_clicked(self):

        score2, f = score.CorrelationChroma3(fileName2,fileName3)

        self.score_text.append(str(score2))

        newfont = QtGui.QFont("Sans Serif", 28, QtGui.QFont.Bold) 



        self.score_done.setText('Similarity found!')
        self.score_done.setStyleSheet('color: #32936F')
        self.score_done.setFont(newfont)

        





app = QtWidgets.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()