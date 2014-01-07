# -*- coding: utf-8 -*-
"""
Very basic 3D graphics example; create a view widget and add a few items.

"""
## Add path to library (just for examples; you do not need this)
import sys
from PySide import QtGui

QString = str
    
import UI_mainWin as ui_template
import zipfile as zip


def open_file():
    fileDialog = QtGui.QFileDialog() 
    fileDialog.FileMode = QtGui.QFileDialog.ExistingFile
    fileDialog.ViewMode = QtGui.QFileDialog.Detail
    root_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/'
    fileName = fileDialog.getOpenFileName(win,"Abrir arquivo de dados", root_file, "Arquivos de dados (*.zip)")
    with zip.ZipFile(fileName[0],'r') as dadosZip:
        listArq = dadosZip.infolist()
        if len(listArq)>0:
            with dadosZip.open(listArq[0].filename) as dados:
                x = []
                y = {}
                foundXLab = False
                for line in dados:
                    wrds = line.split('\t')
                    if wrds[0].strip() == 'X_Value' and not foundXLab:
                        xLabels = wrds[1:-1]
                        for n, lab in enumerate(xLabels):
                            y[n] = []
                        foundXLab = True
                        continue
                    if not foundXLab: continue
                    for n,val in enumerate(wrds):
                        if n == 0: 
                            x += [float(val.replace(',', '.'))]
                            continue
                        y[n - 1] += [float(val.replace(',', '.'))]

    p1 = ui.graphicsView.plotItem
    p1.addLegend((50,50))
    p1.setMenuEnabled()
    for serie, vals in y.iteritems():
        p1.plot(x, vals, pen = (serie, len(xLabels)), name='Channel {0}'.format(serie))    
    p1.showLabel('right')
    ui.statusbar.showMessage('Displaying file:{0}'.format(fileName[0]))

app = QtGui.QApplication([])
win = QtGui.QMainWindow()
win.setWindowTitle('Signal Plotter')
ui = ui_template.Ui_MainWindow()
ui.setupUi(win)
ui.statusbar.showMessage('Ready')
ui.actionOpen.triggered.connect(open_file)
win.show()
sys.exit(app.exec_())