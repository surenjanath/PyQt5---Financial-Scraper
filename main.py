import sys
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication
##from WelcomeScreenUI import Ui_MainWindow
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QSize,QThread, pyqtSignal
import webbrowser

# Scrape libraries
import requests
from bs4 import BeautifulSoup as bs
import string
import random
import time


class ScrapeData(QThread):
  SigData = pyqtSignal(dict)
  
  def __init__(self, search, WClass, parent = None):
    QThread.__init__(self, parent)
    self.data = []
    self.search = search
    self.WClass = WClass

  def run(self):
    search = self.search
    if search == '00':
      lLink = random.choice(string.ascii_letters)
    else:
      lLink = search[0]
    url = f'http://eoddata.com/stocklist/NASDAQ/{lLink}.htm'
    page = requests.get(url)
    if page.status_code == 200:
      soup = bs(page.content,'lxml')
      content = soup.find('div',{'id':'ctl00_cph1_divSymbols'})
      rows = content.find_all('tr')
      for row in rows[1:]:
        contents = row.find_all('td')
        terms = []
        for x in contents:
          terms.append(x.text.strip())
          
        self.data.append({
          'Code'   :    str(terms[0]),	
          'Name'   :    str(terms[1]),
          'High'   :	str(terms[2]),
          'Low'    :	str(terms[3]),
          'Close'  :	str(terms[4]),
          'Volume' :	str(terms[5]),
            })
    try:
      Name = [x['Code'] for x in self.data]
      if search == '00':
        self.WClass.update.setText('Random NasDaq Code generated')
        self.SigData.emit( self.data[random.randint(0, len(self.data))])
      else:
        self.WClass.update.setText('Found : %a' %search)
        self.SigData.emit( self.data[Name.index(search)])
        
    except ValueError :
      self.WClass.update.setText('Please Check Code')
      self.SigData.emit( {
          'Code'   :    search,	
          'Name'   :    'NaN',
          'High'   :	'NaN',
          'Low'    :	'NaN',
          'Close'  :	'NaN',
          'Volume' :	'NaN',
           
            })

class WelcomeScreen(QMainWindow):
  def __init__(self):
    super(WelcomeScreen, self).__init__()
    loadUi("WelcomeScreen.ui",self)
##    self.setupUi(self)
    
    self.Start.show()
    
    #HIDE LABELS
    self.End.hide()
    self.signature.hide()
    self.label_5.hide()
    
    #BTNS CONNECT
    self.Start.clicked.connect(self.gotoShow)
    self.End.clicked.connect(self.gotoHide)
    self.btn_search.clicked.connect(self.gotoScrape)
    self.Closed.clicked.connect(self.exitprogram)
    self.fButton.clicked.connect(self.facebook)
    self.tButton.clicked.connect(self.twitter)
    self.iButton.clicked.connect(self.LinkedIn)
    
    self.SEARCH.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25,xOffset=3,yOffset=3))                                   
    self.label.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25,xOffset=3,yOffset=3))                                   
    self.Start.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=10,xOffset=3,yOffset=3))                                   
    self.btn_search.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=10,xOffset=3,yOffset=3))                                   
    self.End.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=10,xOffset=3,yOffset=3))                                   
    self.progressBar.hide()
    
    #DRAG WINDOW CONNECTORS
    self.__press_pos = None
    self.adjustSize()  # update self.rect() now
    self.move(QApplication.instance().desktop().screen().rect().center() - self.rect().center())
    
  def gotoHide(self):
    #ANIMATION FOR HIDING SEARCH
    self.animation = QPropertyAnimation(self.SEARCH, b"size")
    self.animation.setDuration(200)
    self.animation.setEndValue(QSize(0,330))
    self.animation.setEasingCurve(QEasingCurve.InOutQuad)
    self.animation.start()
    
    self.label_4.setText('NasDaq')
    self.Start.show()
    
    self.label_10.show()
    self.signature.hide()
    self.label_5.hide()
    self.End.hide()
    
    #CLEAR DATAS
    self.Search.clear()
    self.Code.setText(' ')
    self.Close.setText(' ')
    self.High.setText(' ')
    self.Low.setText(' ')
    self.Name.setText(' ')
    self.update.setText('')
    self.Volume.setText(' ')

  def gotoShow(self):
    self.label_10.hide()
    self.label_5.show()
    self.signature.show()
    self.label_4.setText('A little bit me')
    
    #ANIMATION FOR SHOWING SEARCH 
    self.animation = QPropertyAnimation(self.SEARCH, b"size")
    self.animation.setDuration(1000)
    self.animation.setEndValue(QSize(260,330))
    self.animation.setEasingCurve(QEasingCurve.InOutQuad)
    self.animation.start()
    self.Start.hide()
    self.End.show()
    
  def gotoScrape(self):
    self.update.setText('Please Wait...')
    text = self.Search.text().strip().upper()
    
    if len(text)>0:
      pass
    else:
      text = '00'
      
    #Load ScrapeClass   
    self.ScrapeClass = ScrapeData(search = text,WClass = self)  
    self.ScrapeClass.SigData.connect(self.setTexts)
    self.ScrapeClass.start()

  def setTexts(self,info):
    self.Name.setText(' '+  info['Name'])
    self.Code.setText(' ' + info['Code'])
    self.Close.setText(' '+ info['Close'])
    self.High.setText(' '+  info['High'])
    self.Low.setText(' '+   info['Low'])
    self.Volume.setText(' '+info['Volume'])
    
  #DRAGGABLE FUNCTIONS 
  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.__press_pos = event.pos()  # remember starting position

  def mouseReleaseEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.__press_pos = None

  def mouseMoveEvent(self, event):
    if self.__press_pos:  # follow the mouse
      self.move(self.pos() + (event.pos() - self.__press_pos))
      
  #SOCIAL FUNCTIONS  
  def facebook(self):
    webbrowser.open('https://www.facebook.com/surenjanath.singh/')
    
  def twitter(self):
    webbrowser.open('https://twitter.com/surenjanath')
    
  def LinkedIn(self):
    webbrowser.open('https://www.linkedin.com/in/surenjanath/')
    
  def exitprogram(self):
    sys.exit()

if __name__=="__main__":
    
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    welcome.setWindowFlags(Qt.FramelessWindowHint)
    welcome.setAttribute(Qt.WA_TranslucentBackground)
    welcome.setFixedHeight(418)
    welcome.setFixedWidth(800)
    welcome.show()
    try:
        sys.exit(app.exec_())
    except:
        pass

