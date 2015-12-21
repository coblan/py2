from PyQt4 import QtGui, Qsci

class Window(Qsci.QsciScintilla):
    def __init__(self):
        super(Window,self).__init__()
        self.setMarginLineNumbers(1,True)
        font = QtGui.QFont()
        self.setMarginsFont(font)
        fontmetrics = QtGui.QFontMetrics(font)
        self.setMarginWidth(1, fontmetrics.width("00000") + 6)
        self.setAutoIndent(True)
        lexer = Qsci.QsciLexerHTML(self)
        api = Qsci.QsciAPIs(lexer)
        api.add('aLongString')
        api.add('aLongerString')
        api.add('aDifferentString')
        api.add('sOmethingElse')
        api.prepare()
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(Qsci.QsciScintilla.AcsAPIs)
        self.setLexer(lexer)
        self.setUtf8(True)

if __name__ == "__main__":

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()