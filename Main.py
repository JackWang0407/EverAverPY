# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, QtWebKit
from lxml import html
import multiprocessing

import youtube_dl

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


import codecs
import os
import sys
import requests
from bs4 import BeautifulSoup
import urllib
import time
import re
import json
from selenium import webdriver
import progressbar


global OpenloadVedioPath
global OpenloadVedioTitle

def pushButtononClick():
    if Check7MMTV() == "PASS":
        if len(unicode(win.lineEdit.text())) is not 0:
            print "Search and rename"
            win.pushButton_4.setEnabled(True)
        else:
            print "Search Only"
    else:
        win.pushButton_3.setText(_translate("MainWindow", "無番號資訊", None))

    if CheckSDDPOAV() == "PASS":
        win.pushButton_3.setEnabled(True)
    else:
        win.pushButton_3.setText(_translate("MainWindow", "無片源", None))

def CheckSDDPOAV():
    keyword = unicode(win.lineEdit_2.text())
    #print keyword
    res = requests.get('http://sddpoav.com/?s=' + keyword)
    if res.status_code == requests.codes.ok:
        html = res.content
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find('div', attrs={'class': 'video'})
        if data is not None:
            if data.find('a') is not None:
                href = data.find('a').get('href')
            else:
                print "Cannot Find this AV Number - - http://sddpoav.com/"
                return 1
        else:
            print "Cannot Find this AV Number - - http://sddpoav.com/"
            return 1
        res = requests.get(href)
        if res.status_code == requests.codes.ok:
            html = res.content
            soup = BeautifulSoup(html, 'html.parser')
            video_path = soup.find('div', attrs={'class': 'video_code'}).find('iframe').get('src')
            print video_path
            ydl = youtube_dl.YoutubeDL()
            with ydl:
                youtube_dlresult = ydl.extract_info(
                    video_path,
                    download=False  # !!We just want to extract the info
                )
            if 'entries' in youtube_dlresult:
            # Can be a playlist or a list of videos
                video = youtube_dlresult['entries'][0]
            else:
            # Just a video
                video = youtube_dlresult
            #print(video)
            video_url = video['url']
            global OpenloadVedioPath
            global OpenloadVedioTitle
            OpenloadVedioPath = video_url
            OpenloadVedioTitle = video['title']
            #print OpenloadVedioPath
            #print OpenloadVedioTitle


    else:
        print str(res.status_code)
        return -1

    return "PASS"

def CheckPORN68JAV():
    keyword = unicode(win.lineEdit_2.text())
    res = requests.get('http://porn68jav.com/?s=' + keyword)
    if res.status_code == requests.codes.ok:
        html = res.content
        soup = BeautifulSoup(html, 'html.parser')
        print '----------------'
        data = soup.find('div', attrs={'class': 'data'})
        if data is not None:
            entry_title = data.find('', attrs={'class': 'entry-title'})
            if entry_title is not None:
                #print entry_title
                print entry_title.find('a').get('href')
            else:
                print "Cannot Find this AV Number - - http://porn68jav.com"
                return -1
        else:
            print "Cannot Find this AV Number - - http://porn68jav.com"
            return -1
    res = requests.get(entry_title.find('a').get('href'))
    if res.status_code == requests.codes.ok:
        #print(str(res.status_code) + " OK")
        #print(res.content)
        html = res.content
        soup = BeautifulSoup(html, 'html.parser')
        print '----------------'
        title = soup.find('div', attrs={'class': 'inner cf'})
        print title.find('', attrs={'class': 'entry-title'}).text
        print soup.find(text=re.compile(u'発売日')).replace(u"発売日：", "").replace(u"\n","")
        win.lineEdit_10.setText(
            _translate("MainWindow", soup.find(text=re.compile(u'発売日')).replace(u"発売日：", "").replace(u"\n", ""), None))

        print soup.find(text=re.compile(u'収録時間')).replace(u"収録時間：", "").replace(u"\n","")
        win.lineEdit_9.setText(
            _translate("MainWindow", soup.find(text=re.compile(u'収録時間')).replace(u"収録時間：", "").replace(u"\n", ""),
                       None))
        print soup.find(text=re.compile(u'出演者')).replace(u"出演者：", "").replace(u"\n","")
        win.lineEdit_3.setText(
            _translate("MainWindow", soup.find(text=re.compile(u'出演者')).replace(u"出演者：", "").replace(u"\n", ""),
                       None))

        print soup.find(text=re.compile(u'監督')).replace(u"監督：", "").replace(u"\n","")
        win.lineEdit_6.setText(
            _translate("MainWindow", soup.find(text=re.compile(u'監督')).replace(u"監督：", "").replace(u"\n", ""), None))
        print soup.find(text=re.compile(u'メーカー')).replace(u"メーカー：", "").replace(u"\n", "")
        win.lineEdit_5.setText(
            _translate("MainWindow", soup.find(text=re.compile(u'メーカー')).replace(u"メーカー：", "").replace(u"\n", ""),
                       None))

    return "PASS"

def Check7MMTV():
    res = requests.post('https://7mm.tv/zh/searchform_search/all/index.html',
                        data={'search_keyword': unicode(win.lineEdit_2.text()), 'search_type': 'censored',
                        'op': 'search'})
    if res.status_code == requests.codes.ok:
        html = res.content
        soup = BeautifulSoup(html, 'html.parser')
        print '----------------'
        topic_area = soup.find('div', attrs={'class': 'topic_area'})
        topic_box = topic_area.find('div', attrs={'class': 'topic_box'})
        if topic_area is not None:
            if topic_box is not None:
                print topic_box.find('a').get('href')
            else:
                print "Cannot Find this AV Number - - https://7mm.tv"
                return -1
        else:
            print "Cannot Find this AV Number - - https://7mm.tv"
            return -1
        res = requests.get(topic_box.find('a').get('href'))
        if res.status_code == requests.codes.ok:
            html = res.content
            soup = BeautifulSoup(html, 'html.parser')
            contents_title = soup.find('div', attrs={'id': 'contents_title'})
            contents_title = contents_title.find('b').text
            print contents_title
            print '----------------'
            for mvinfo_dmm_A in soup.find_all('div', attrs={'class': 'mvinfo_dmm_A'}):
                if mvinfo_dmm_A.find('b').text == u"番號：":
                    print mvinfo_dmm_A.text.lstrip(u"番號：")
                    number = mvinfo_dmm_A.text.lstrip(u"番號：")
                    win.lineEdit_8.setText(_translate("MainWindow", mvinfo_dmm_A.text.lstrip(u"番號："), None))
                    rm_string = "["+mvinfo_dmm_A.text.lstrip(u"番號：")+"]"
                    contents_title = contents_title.replace(rm_string, "")
                    print contents_title
                if mvinfo_dmm_A.find('b').text == u"發行日期：":
                    print mvinfo_dmm_A.text.lstrip(u"發行日期：")
                    date = mvinfo_dmm_A.text.lstrip(u"發行日期：")
                    win.lineEdit_10.setText(_translate("MainWindow", mvinfo_dmm_A.text.lstrip(u"發行日期："), None))
                if mvinfo_dmm_A.find('b').text == u"影片時長：":
                    print mvinfo_dmm_A.text.lstrip(u"影片時長：")
                    win.lineEdit_9.setText(_translate("MainWindow", mvinfo_dmm_A.text.lstrip(u"影片時長："), None))
                if mvinfo_dmm_A.find('b').text == u"導演：":
                    print mvinfo_dmm_A.text.lstrip(u"導演：")
                    win.lineEdit_6.setText(_translate("MainWindow", mvinfo_dmm_A.text.lstrip(u"導演："), None))
                if mvinfo_dmm_A.find('b').text == u"製作商：":
                    print mvinfo_dmm_A.text.lstrip(u"製作商：")
                    win.lineEdit_5.setText(_translate("MainWindow", mvinfo_dmm_A.text.lstrip(u"製作商："), None))
                if mvinfo_dmm_A.find('b').text == u"發行商：":
                    print mvinfo_dmm_A.text.lstrip(u"發行商：")
                    win.lineEdit_4.setText(_translate("MainWindow", mvinfo_dmm_A.text.lstrip(u"發行商："), None))
            mvinfo_introduction = soup.find('div', attrs={'class': 'mvinfo_introduction'}).text
            win.textEdit.setText(_translate("MainWindow", mvinfo_introduction, None))
            win.lineEdit_3.setText('')
            avers=""
            for av_performer_name_box in soup.find_all('div', attrs={'class': 'av_performer_name_box'}):
                #print av_performer_name_box.text
                contents_title = contents_title.replace(av_performer_name_box.text, "")
                avers += av_performer_name_box.text+","
            print avers.strip(",")
            win.textEdit_2.setText(_translate("MainWindow", contents_title, None))
            win.lineEdit_3.insert(_translate("MainWindow", avers.strip(","), None))
            win.lineEdit_11.setText(
                _translate("MainWindow", "[" + number + "] " + contents_title + " - " + avers.strip(",") + " - " + date,
                           None))
            print '----------------'
            img = soup.find('img').get('src')
            print "Download from ",img,".."
            urllib.urlretrieve(img, 'tmp.jpg')
            time.sleep(1)
            tmp_img = QtGui.QPixmap("tmp.jpg").scaled(win.label_18.width(), win.label_18.height())
            win.label_18.setPixmap(tmp_img)
            #win.pushButton_4.setEnabled(True)
            return "PASS"

def pushButton_4onClick():
    #print "pushButton_4onClick"
    #print win.lineEdit.text()
    FilePath = unicode(win.lineEdit.text())
    Filename = os.path.basename(FilePath)
    FileSubname = os.path.splitext(Filename)[1]
    Filename = os.path.splitext(Filename)[0]
    FilePath = os.path.dirname(FilePath)+"/"
    #print "FilePath = "+FilePath
    #print "Filename = "+Filename
    #print "FileSubname = "+FileSubname
    NewFilename = unicode(win.lineEdit_11.text())
    #print NewFilename
    NewNumber = unicode(win.lineEdit_8.text())
    #print FilePath + NewNumber
    #print FilePath + NewFilename + FileSubname
    #print FilePath + NewFilename+".jpg"
    os.mkdir(FilePath + NewNumber)
    os.rename("tmp.jpg", FilePath + NewNumber + "/" + NewFilename + ".jpg")
    os.rename(unicode(win.lineEdit.text()), FilePath + NewNumber + "/" + NewFilename + FileSubname)
    win.pushButton_4.setEnabled(False)

def pushButton_3onClick():
    print "pushButton_3onClick"
    global OpenloadVedioPath
    global OpenloadVedioTitle
    #print OpenloadVedioPath
    #print OpenloadVedioTitle
    ydl = youtube_dl.YoutubeDL({'outtmpl': OpenloadVedioTitle})
    with ydl:
        youtube_dlresult = ydl.extract_info(
            OpenloadVedioPath,
            download=True  # !!We just want to extract the info
        )
    win.pushButton_3.setEnabled(False)

class Ui_MainWindow(QtGui.QMainWindow):

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        st = str(event.mimeData().urls())
        st = st.replace("[PyQt4.QtCore.QUrl(u'file:///", "")
        st = st.replace("'), ", ",")
        st = st.replace("PyQt4.QtCore.QUrl(u'file:///", "")
        st = st.replace("')]", "")
        st = st.decode('unicode_escape')
        win.lineEdit.setText(_translate("MainWindow", st, None))
        #win.label_19.setText(_translate("MainWindow", st, None))
        print os.path.basename(st)
        win.lineEdit_2.setText(os.path.splitext(os.path.basename(st))[0])

        pushButtononClick()



    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1070, 831)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 1051, 91))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(90, 30, 521, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(620, 30, 71, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(830, 20, 91, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_3 = QtGui.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(830, 55, 91, 31))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_2 = QtGui.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(930, 20, 75, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(700, 30, 121, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 110, 1051, 461))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(620, 30, 40, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(620, 130, 40, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(620, 180, 40, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(830, 180, 40, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(620, 280, 40, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(830, 230, 41, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(620, 230, 40, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(620, 330, 41, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.lineEdit_3 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(620, 150, 411, 20))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.lineEdit_4 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(620, 200, 201, 20))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit_5 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(830, 200, 201, 20))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.lineEdit_6 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(830, 250, 201, 20))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.lineEdit_7 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_7.setGeometry(QtCore.QRect(620, 250, 201, 20))
        self.lineEdit_7.setObjectName(_fromUtf8("lineEdit_7"))
        self.lineEdit_8 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_8.setGeometry(QtCore.QRect(620, 300, 201, 20))
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))
        self.label_12 = QtGui.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(920, 280, 61, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(830, 280, 41, 16))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.lineEdit_9 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_9.setGeometry(QtCore.QRect(830, 300, 81, 20))
        self.lineEdit_9.setObjectName(_fromUtf8("lineEdit_9"))
        self.lineEdit_10 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_10.setGeometry(QtCore.QRect(920, 300, 111, 20))
        self.lineEdit_10.setObjectName(_fromUtf8("lineEdit_10"))
        self.textEdit = QtGui.QTextEdit(self.groupBox_2)
        self.textEdit.setGeometry(QtCore.QRect(620, 350, 411, 101))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit_2 = QtGui.QTextEdit(self.groupBox_2)
        self.textEdit_2.setGeometry(QtCore.QRect(620, 50, 411, 71))
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.label_14 = QtGui.QLabel(self.groupBox_2)
        self.label_14.setGeometry(QtCore.QRect(10, 30, 40, 16))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_18 = QtGui.QLabel(self.groupBox_2)
        self.label_18.setGeometry(QtCore.QRect(10, 50, 600, 400))
        self.label_18.setText(_fromUtf8(""))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 580, 1051, 121))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)

        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.label_15 = QtGui.QLabel(self.groupBox_3)
        self.label_15.setGeometry(QtCore.QRect(20, 30, 71, 16))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtGui.QLabel(self.groupBox_3)
        self.label_16.setGeometry(QtCore.QRect(20, 60, 71, 16))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_17 = QtGui.QLabel(self.groupBox_3)
        self.label_17.setGeometry(QtCore.QRect(20, 90, 71, 16))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.lineEdit_11 = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_11.setGeometry(QtCore.QRect(100, 30, 621, 20))
        self.lineEdit_11.setObjectName(_fromUtf8("lineEdit_11"))
        self.lineEdit_12 = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_12.setGeometry(QtCore.QRect(100, 60, 621, 20))
        self.lineEdit_12.setObjectName(_fromUtf8("lineEdit_12"))
        self.checkBox = QtGui.QCheckBox(self.groupBox_3)
        self.checkBox.setGeometry(QtCore.QRect(740, 30, 131, 16))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox_3)
        self.checkBox_2.setGeometry(QtCore.QRect(740, 60, 131, 16))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox_3)
        self.checkBox_3.setGeometry(QtCore.QRect(740, 90, 131, 16))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.pushButton_4 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_4.setGeometry(QtCore.QRect(880, 30, 151, 71))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.groupBox_4 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 710, 1051, 80))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.groupBox_4.setFont(font)
        self.label_19 = QtGui.QLabel(self.groupBox_4)
        self.label_19.setGeometry(QtCore.QRect(10, 20, 1031, 41))
        self.label_19.setText(_fromUtf8(""))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.groupBox_2.raise_()
        self.groupBox.raise_()
        self.groupBox_3.raise_()
        self.groupBox_4.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1070, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_4.setEnabled(False)
        self.pushButton_3.setEnabled(False)
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "捷克練習", None))
        self.groupBox.setTitle(_translate("MainWindow", "搜尋目標", None))
        self.label.setText(_translate("MainWindow", "檔案路徑", None))
        self.label_2.setText(_translate("MainWindow", "快速查詢", None))
        self.label_3.setText(_translate("MainWindow", "搜尋品番", None))
        self.pushButton.setText(_translate("MainWindow", "開始搜尋", None))
        self.pushButton_3.setText(_translate("MainWindow", "加入下載", None))
        self.pushButton_2.setText(_translate("MainWindow", "設定", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "搜尋結果", None))
        self.label_4.setText(_translate("MainWindow", "片名", None))
        self.label_5.setText(_translate("MainWindow", "演員", None))
        self.label_6.setText(_translate("MainWindow", "公司", None))
        self.label_7.setText(_translate("MainWindow", "廠商", None))
        self.label_8.setText(_translate("MainWindow", "品番", None))
        self.label_9.setText(_translate("MainWindow", "導演", None))
        self.label_10.setText(_translate("MainWindow", "系列", None))
        self.label_11.setText(_translate("MainWindow", "簡介", None))
        self.label_12.setText(_translate("MainWindow", "發售日", None))
        self.label_13.setText(_translate("MainWindow", "片長", None))
        self.label_14.setText(_translate("MainWindow", "封面", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "重新命名", None))
        self.label_15.setText(_translate("MainWindow", "目錄結構", None))
        self.label_16.setText(_translate("MainWindow", "命名模式", None))
        self.label_17.setText(_translate("MainWindow", "結果預覽", None))
        self.label_18.setText(_translate("MainWindow", "", None))
        self.checkBox.setText(_translate("MainWindow", "建立階層目錄", None))
        self.checkBox_2.setText(_translate("MainWindow", "建立同名目錄", None))
        self.checkBox_3.setText(_translate("MainWindow", "同步移動封面", None))
        self.pushButton_4.setText(_translate("MainWindow", "重新命名", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "搜尋狀態", None))

    def buttons_action(self, MainWindow):
        self.pushButton.clicked.connect(pushButtononClick)
        self.pushButton_4.clicked.connect(pushButton_4onClick)
        self.pushButton_3.clicked.connect(pushButton_3onClick)

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.buttons_action(self)

app = QtGui.QApplication(sys.argv)
app.addLibraryPath("venv\Lib\site-packages\PyQt4\plugins")
win = Ui_MainWindow()
win.show()
win.setAcceptDrops(True)
sys.exit(app.exec_())
