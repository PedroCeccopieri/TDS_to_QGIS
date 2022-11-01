from qgis.utils import iface
from PyQt5.QtCore import Qt, QDateTime, QUrl
from PyQt5.QtWidgets import QFileDialog

from pathlib import Path
import tempfile

class windowView():

    def __init__(self, wnd):

        self.wnd = wnd
        self.tempDir = Path(tempfile.gettempdir())
        self.wnd.tempLineEdit.setText(str(self.tempDir))


    def showWindow(self):

        iface.mainWindow().addDockWidget(Qt.LeftDockWidgetArea, self.wnd)

    def browseJson(self):

        fileName = QFileDialog.getOpenFileName(self.wnd, "Open File", '', 'JSON (*.json)')
        self.wnd.jsonLineEdit.setText(fileName[0])

    def browseTempDir(self):

        dirName = QFileDialog.getExistingDirectoryUrl(self.wnd, "Choose the directory")
        if not (dirName.isEmpty()):
            self.tempDir = Path(dirName.toLocalFile())
            self.wnd.tempLineEdit.setText(str(self.tempDir))

    def addNamesComboBox(self, names = None):

        self.wnd.comboBox.clear()

        if (names):

            for name in names:
                self.wnd.comboBox.addItem(name)

    def isDepthEnable(self):

        return self.wnd.maxDepthBox.isEnabled()

    def getMaxDateTime(self):

        return self.wnd.maxDateTime.dateTime()

    def getMinDateTime(self):

        return self.wnd.minDateTime.dateTime()

    def getMaxLongitude(self):

        return self.wnd.maxLongitudeBox.value()

    def getMinLongitude(self):

        return self.wnd.minLongitudeBox.value()

    def getMaxLatitude(self):

        return self.wnd.maxLatitudeBox.value()

    def getMinLatitude(self):

        return self.wnd.minLatitudeBox.value()

    def getMaxDepth(self):

        return self.wnd.maxDepthBox.value()

    def getMinDepth(self):

        return self.wnd.minDepthBox.value()

    def getVariables(self):

        return self.wnd.variableList.selectedItems()

    def getCheckBoxState(self):

        return self.wnd.checkBox.checkState()

    def getCurrentDatasetName(self):

        return self.wnd.comboBox.currentText()

    def getJsonUrl(self):

        return self.wnd.jsonLineEdit.text()

    def setDateTimeEnabled(self, val):

        self.wnd.minDateTime.setEnabled(val)
        self.wnd.maxDateTime.setEnabled(val)

    def setLatitudeEnabled(self, val):

        self.wnd.minLatitudeBox.setEnabled(val)
        self.wnd.maxLatitudeBox.setEnabled(val)

    def setLongitudeEnabled(self, val):

        self.wnd.minLongitudeBox.setEnabled(val)
        self.wnd.maxLongitudeBox.setEnabled(val)

    def setDepthEnabled(self, val):

        self.wnd.minDepthBox.setEnabled(val)
        self.wnd.maxDepthBox.setEnabled(val)

    def setDateTimeZero(self):

        zero = QDateTime.fromString("2000-01-01T00:00:00Z","yyyy-MM-ddTHH:mm:ssZ")

        self.wnd.minDateTime.setDateTimeRange(zero, zero)
        self.wnd.maxDateTime.setDateTimeRange(zero, zero)

    def setLongitudeZero(self):

        self.wnd.minLongitudeBox.setRange(0, 0)
        self.wnd.maxLongitudeBox.setRange(0, 0)

    def setLatitudeZero(self):

        self.wnd.minLatitudeBox.setRange(0, 0)
        self.wnd.maxLatitudeBox.setRange(0, 0)

    def setDepthZero(self):

        self.wnd.minDepthBox.setRange(0, 0)
        self.wnd.maxDepthBox.setRange(0, 0)

    def setVariablesClear(self):

        self.wnd.variableList.clear()

    def setDateTimeLimits(self, minDate, maxDate):

        aa = QDateTime.fromString(minDate,"yyyy-MM-ddTHH:mm:ssZ")
        bb = QDateTime.fromString(maxDate,"yyyy-MM-ddTHH:mm:ssZ")

        self.wnd.minDateTime.setDateTimeRange(aa, bb)
        self.wnd.maxDateTime.setDateTimeRange(aa, bb)

        self.wnd.minDateTime.setDateTime(aa)
        self.wnd.maxDateTime.setDateTime(bb)

    def setLongitudeLimits(self, minLon, maxLon):

        self.wnd.minLongitudeBox.setRange(minLon, maxLon)
        self.wnd.maxLongitudeBox.setRange(minLon, maxLon)

        self.wnd.minLongitudeBox.setValue(minLon)
        self.wnd.maxLongitudeBox.setValue(maxLon)

    def setLatitudeLimits(self, minLat, maxLat):

        self.wnd.minLatitudeBox.setRange(minLat, maxLat)
        self.wnd.maxLatitudeBox.setRange(minLat, maxLat)

        self.wnd.minLatitudeBox.setValue(minLat)
        self.wnd.maxLatitudeBox.setValue(maxLat)

    def setDepthLimits(self, minDep, maxDep):

        self.wnd.minDepthBox.setRange(minDep, maxDep)
        self.wnd.maxDepthBox.setRange(minDep, maxDep)

        self.wnd.minDepthBox.setValue(minDep)
        self.wnd.maxDepthBox.setValue(maxDep)

    def setVariblesNames(self, varNames):

        self.wnd.variableList.addItems(varNames)
