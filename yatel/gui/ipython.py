#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice 
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.

# Based on: http://stackoverflow.com/questions/11513132


#===============================================================================
# DOCS
#===============================================================================

"""Wraper around IPython

"""

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
# INIT OF IPYTHON KERNEL
#===============================================================================

def _event_loop(kernel):
    kernel.timer = QtCore.QTimer()
    kernel.timer.timeout.connect(kernel.do_one_iteration)
    kernel.timer.start(1000*kernel._poll_interval)

_kernel_app = None
_kernel_app = IPKernelApp.instance()
_kernel_app.initialize(['python', '--pylab=qt'])
_kernel_app.kernel.eventloop = _event_loop

_connection_file = find_connection_file(_kernel_app.connection_file)
_manager = QtKernelManager(connection_file=_connection_file)
_manager.load_connection_file()
_manager.start_channels()
atexit.register(_manager.cleanup_connection_file)


#===============================================================================
# CLASS
#===============================================================================

class IPythonWidget(RichIPythonWidget):
    """IPython console connected to the default kernel embeddable in *Qt*.
    
    Nota: if you have 2 instances of this class is shared console.
    
    """

    def __init__(self):
        """Creates a new instance of ``IPythonWidget``.
        
        """
        try: # Ipython v0.13
            super(IPythonWidget, self).__init__(gui_completion='droplist')
        except TraitError:  # IPython v0.12
            super(IPythonWidget, self).__init__(gui_completion=True)
            widget = RichIPythonWidget(gui_completion=True)
        self.kernel_manager = _manager
        _kernel_app.start()
    
    def reset_ns(self, **kwargs):
        """Reset all commands and locals variables of the shell and setup anew
        vars on the namespace.
        
        **Params**
            :**kwargs: Variables to be seted in the namespace.
            
        """
        _kernel_app.shell.reset()
        _kernel_app.shell.user_ns.update(kwargs)
        
    def write(self, msg):
        """Write the ``msg`` in the console."""
        _kernel_app.shell.write(msg)
        
    def destroy(self):
        """Reset all commands and locals variables of the shell and destroy
        this widget."""
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
