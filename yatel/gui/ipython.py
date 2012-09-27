#!/usr/bin/env python
# -*- coding: utf-8 -*-

# THIS CODE FOUND AT: http://stackoverflow.com/questions/11513132/embedding-ipython-qt-console-in-a-pyqt-application

#===============================================================================
# IMPORTS
#===============================================================================

import atexit

from IPython.zmq.ipkernel import IPKernelApp
from IPython.lib.kernel import find_connection_file
from IPython.frontend.qt.kernelmanager import QtKernelManager
from IPython.frontend.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.utils.traitlets import TraitError

from PyQt4 import QtGui
from PyQt4 import QtCore


#===============================================================================
# INIT
#===============================================================================

def event_loop(kernel):
    kernel.timer = QtCore.QTimer()
    kernel.timer.timeout.connect(kernel.do_one_iteration)
    kernel.timer.start(1000*kernel._poll_interval)


_kernel_app = None
_kernel_app = IPKernelApp.instance()
_kernel_app.initialize(['python', '--pylab=qt'])
_kernel_app.kernel.eventloop = event_loop

_connection_file = find_connection_file(_kernel_app.connection_file)
_manager = QtKernelManager(connection_file=_connection_file)
_manager.load_connection_file()
_manager.start_channels()
atexit.register(_manager.cleanup_connection_file)

#===============================================================================
# CLASS
#===============================================================================

class IPythonWidget(RichIPythonWidget):

    def __init__(self):
        try: # Ipython v0.13
            super(IPythonWidget, self).__init__(gui_completion='droplist')
        except TraitError:  # IPython v0.12
            super(IPythonWidget, self).__init__(gui_completion=True)
            widget = RichIPythonWidget(gui_completion=True)
        self.kernel_manager = _manager
        _kernel_app.start()
    
    def reset_ns(self, **kwargs):
        _kernel_app.shell.reset()
        _kernel_app.shell.user_ns.update(kwargs)
        
    def destroy(self):
        _kernel_app.shell.reset()
        super(IPythonWidget, self).destroy()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
    app = QtGui.QApplication([''])
    widget = IPythonWidget()
    widget.reset_ns(k=_kernel_app)
    widget.show()
    app.exec_()
