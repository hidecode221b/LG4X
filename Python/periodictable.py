import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QCheckBox
from PyQt5.QtCore import pyqtSignal
from periodictableui import Ui_PeriodicTable
from elements import Transition
from elementdata import ElementData

class PeriodicTable(QWidget):

    # Custom signal defined here
    elementEmitted = pyqtSignal(object, bool)

    def __init__(self):
        super().__init__()

        self.ui = Ui_PeriodicTable()
        self.ui.setupUi(self)

        # Element Objects
        self.elements = ElementData().xps
        self.periodicTable = {}
        self.selectedElements = []

        for element in self.elements:
            #self.periodicTable[element['symbol']] = Element(element['mass'], element['symbol'], element['name'], element['number'], element['alka'])
            self.periodicTable[element['symbol']] = Transition(element['symbol'], element['alka'], element['aes'])
            #print(element['symbol'])

        # Iterates through all of the UI object names and connects slots/signals
        # This widget is highly dependent on the naming convention of the buttons
        # and line edits, changing the names will break the function assignments
        for name in dir(self.ui):
            # Element buttons:
            if 'ebtn' in name:
                btn = getattr(self.ui, name)
                btn.clicked[bool].connect(self.emitElement)

    # Slot for element button clicked signal
    # Emits custom signal with elemental symbol and boolean
    def emitElement(self, checked):
        symbol = self.sender().text()
        elementObject = self.periodicTable[symbol]
        self.elementEmitted.emit(elementObject, checked)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PeriodicTable()
    window.show()
    sys.exit(app.exec_())
