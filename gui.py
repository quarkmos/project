import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton
from PyQt5.QtGui import QIcon #윈도우아이콘
from PyQt5.QtCore import QCoreApplication #버튼


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('tomato for you') #윈도우 창 이름

####버튼####
        nextbt = QPushButton('Quit', self)
        nextbt.move(50, 50)
        nextbt.resize(nextbt.sizeHint())
        nextbtn.clicked.connect(QCoreApplication.instance().quit)
####윈도우####        
        self.center() #화면의 중앙
        self.resize(1000, 500) #윈도우 사이즈
        self.show() #윈도우 보여주기
        self.setWindowIcon(QIcon('C:\\Users\\quarkmos\\Desktop\\project\\tomatoicon.png'))
####화면중앙####         
    def center(self):
        qr = self.frameGeometry() #frameGeometry() 메서드를 이용해서 창의 위치와 크기 정보를 가져옵니다.
        cp = QDesktopWidget().availableGeometry().center() #사용하는 모니터 화면의 가운데 위치를 파악합니다.
        qr.moveCenter(cp) #창의 직사각형 위치를 화면의 중심의 위치로 이동합니다.
        self.move(qr.topLeft()) #현재 창을, 화면의 중심으로 이동했던 직사각형(qr)의 위치로 이동시킵니다. 결과적으로 현재 창의 중심이 화면의 중심과 일치하게 돼서 창이 가운데에 나타나게 됩니다.

####???####
if __name__ == '__main__': # __name__ 현재 모듈의 이름을 저장하는 내장변수
   app = QApplication(sys.argv) #어플리케이션 객체생성
   ex = MyApp() #excute
   sys.exit(app.exec_()) 