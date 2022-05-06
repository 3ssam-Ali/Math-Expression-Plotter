from PyQt5 import QtWidgets, uic, QtGui
import pyqtgraph as pg
import sys
from MathParser import Expression


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('PlotterGui.ui', self)
        # setting up the GraphWidget
        # making the line wider and black
        self._pen = pg.mkPen(color='k', width=2)
        # Get the default window background,
        color = self.palette().color(QtGui.QPalette.Window)
        self.graphWidget.setBackground(color)
        # self.graphWidget.setBackground('w') # setting the graphWidget background to white
        self.graphWidget.showGrid(x=True, y=True)  # showing the Grid lines

        # Connecting the Buttons
        self.OneButton.clicked.connect(lambda: self.addText('1'))
        self.TwoButton.clicked.connect(lambda: self.addText('2'))
        self.ThreeButton.clicked.connect(lambda: self.addText('3'))
        self.FourButton.clicked.connect(lambda: self.addText('4'))
        self.FiveButton.clicked.connect(lambda: self.addText('5'))
        self.SixButton.clicked.connect(lambda: self.addText('6'))
        self.SevenButton.clicked.connect(lambda: self.addText('7'))
        self.EightButton.clicked.connect(lambda: self.addText('8'))
        self.NineButton.clicked.connect(lambda: self.addText('9'))
        self.ZeroButton.clicked.connect(lambda: self.addText('0'))
        self.AddButton.clicked.connect(lambda: self.addText('+'))
        self.SubButton.clicked.connect(lambda: self.addText('-'))
        self.MulButton.clicked.connect(lambda: self.addText('*'))
        self.DivButton.clicked.connect(lambda: self.addText('/'))
        self.PowButton.clicked.connect(lambda: self.addText('^'))
        self.XButton.clicked.connect(lambda: self.addText('x'))
        self.PlotButton.clicked.connect(self.plot)
        # drawing en example graph at start
        self.graphWidget.plot(
            range(101), [(x**2)+1 for x in range(101)], pen=self._pen)

    def addText(self, character):
        '''Add a token to the expression'''
        txt = self.FunTextBox.text()
        self.FunTextBox.setText(txt+character)

    def getExpression(self):
        '''
        Return Expression Object after Validation

        Return:
        ------
            Expr(Expression Object): returns an instance of Expression class

            returns None if the expression is invalid
        '''
        txt = self.FunTextBox.text()
        txt = txt.lower().replace('^', '**')
        try:
            expr = Expression(txt)
        except ValueError as se:  # the expression contains invalid characters
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),
                                          'Invalid Expression', f"Not a valid algebraic expression: {self.FunTextBox.text()}.\nThe expression probably contains invalid characters.")
        except SyntaxError as se:  # the expression is written wrong
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),
                                          'Syntax Error', f"Check your syntax.\nYou may have forgotten a bracket or an operator somewhere.")
        except NameError as ne:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),
                                          'Variable Error', f"Some variable/s in the expression is not recognized")
        except TypeError as te:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),
                                          'Error', f"Only simple expressions allowed.")
        else:
            return expr
        return None

    def emptyWarning(self):
        '''Shows a temporary toolTip warning of empty expression'''
        point = self.pos()+self.FunTextBox.pos()
        QtWidgets.QToolTip.showText(
            point, "This field can't be empty", self.FunTextBox)

    def plot(self):
        '''Plot the expression written in the textBox to the graph'''
        sep=[] # seperator if the graph is partitioned
        if self.FunTextBox.text():
            self.graphWidget.clear()
            lBound = self.LBoundSpinBox.value()
            hBound = self.HBoundSpinBox.value()
            step = self.StepSpinBox.value()
            if expr := self.getExpression():
                xAxis = range(lBound, hBound+1, step)
                yAxis = []
                for i,v in enumerate(xAxis): 
                    try:n = expr.solve({'x': v})
                    except ZeroDivisionError:
                        n = 0
                        sep.append(i)
                    if n > 2**50:
                        QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),
                                                      'Error', f"The Values of f(x) became too large to draw.")
                        break
                    yAxis.append(n)
                else:
                    if sep:
                        if len(sep)==len(xAxis):
                            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),
                                                      'Error', f"Cannot divide by zero.")
                        else:
                            for s in sep:
                                self.graphWidget.plot(xAxis[:s], yAxis[:s], pen=self._pen)
                                self.graphWidget.plot(xAxis[s+1:], yAxis[s+1:], pen=self._pen)
                    else: 
                        self.graphWidget.plot(xAxis, yAxis, pen=self._pen)
        else:
            self.emptyWarning()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.setWindowTitle('Gui Math Plotter')
    main.show()
    sys.exit(app.exec_())
