from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

app = pg.mkQApp("Plotting Example")
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

check1 = QtGui.QCheckBox('lol')
layout = pg.LayoutWidget()

layout.addWidget(check1, 1, 1)
layout.addWidget(win, 2, 1)

layout.resize(800,800)
layout.show()


p6 = win.addPlot(title="Updating plot")
curve = p6.plot(pen='y')
data = np.empty(100)
ptr = 0
def update():
    global data, ptr
    data[ptr] = np.log(ptr+1)
    ptr += 1
    if ptr >= data.shape[0]:
        tmp = data
        data = np.empty(data.shape[0] * 2)
        data[:tmp.shape[0]] = tmp

    if check1.isChecked():
        curve.setData(range(ptr-100, ptr), data[ptr-100:ptr])
    else:
        curve.setData(data[:ptr])
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)



if __name__ == '__main__':
    pg.exec()