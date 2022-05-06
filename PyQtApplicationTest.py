from PyQt5 import QtWidgets, uic, QtGui
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
from LogicTest import MathParser
import re

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.parser=MathParser()
        
        #Load the UI Page
        uic.loadUi('PlotterGui.ui', self)
        # setting up the GraphWidget
        self._pen=pg.mkPen(color='k',width=2) #making the line wider and black
        color = self.palette().color(QtGui.QPalette.Window)  # Get the default window background,
        self.graphWidget.setBackground(color)
        # self.graphWidget.setBackground('w') # setting the graphWidget background to white
        self.graphWidget.showGrid(x=True, y=True) # showing the Grid lines 

        # Connecting the Buttons
        self.OneButton.clicked.connect(lambda : self.addText('1'))
        self.TwoButton.clicked.connect(lambda : self.addText('2'))
        self.ThreeButton.clicked.connect(lambda : self.addText('3'))
        self.FourButton.clicked.connect(lambda : self.addText('4'))
        self.FiveButton.clicked.connect(lambda : self.addText('5'))
        self.SixButton.clicked.connect(lambda : self.addText('6'))
        self.SevenButton.clicked.connect(lambda : self.addText('7'))
        self.EightButton.clicked.connect(lambda : self.addText('8'))
        self.NineButton.clicked.connect(lambda : self.addText('9'))
        self.ZeroButton.clicked.connect(lambda : self.addText('0'))
        self.AddButton.clicked.connect(lambda : self.addText('+'))
        self.SubButton.clicked.connect(lambda : self.addText('-'))
        self.MulButton.clicked.connect(lambda : self.addText('*'))
        self.DivButton.clicked.connect(lambda : self.addText('/'))
        self.PowButton.clicked.connect(lambda : self.addText('^'))
        self.PlotButton.clicked.connect(self.plot)        
        
        # self.plot() # draws the example plot wen starting 

    def addText(self,character):
        txt=self.FunTextBox.text()
        self.FunTextBox.setText(txt+character)
    
    def checkValid(self,expr:str) -> bool:
        '''checks if the string is valid'''
        validChar='1234567890+-/*x() '
        if any([c not in validChar for c in expr]):
            return False
        else: 
            return True

    def getExpression(self):
        expr=self.FunTextBox.text()
        # expr='asad'
        expr=expr.lower().replace('^','**')
        if not self.checkValid(expr):
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),
             'Invalid Expression',f"Not a simple algebraic expression: {expr}.\n x is the only accepted variable ")
            raise ValueError(f"Not a simple algebraic expression: {expr}")
        else:
            return expr
        

    def plot(self):
        self.graphWidget.clear()
        if self.FunTextBox.text():
            expr=self.getExpression()
            lBound=self.LBoundSpinBox.value()
            hBound=self.HBoundSpinBox.value()
            xAxis=range(lBound,hBound+1)
            yAxis=[self.parser.parse(expr,{'x':x}) for x in xAxis]
            self.graphWidget.plot(xAxis, yAxis,pen=self._pen)
        else:
            self.graphWidget.plot(range(101), [(x**2)+1 for x in range(101)],pen=self._pen)
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.setWindowTitle('Gui Math Plotter')
    main.show()
    sys.exit(app.exec_())