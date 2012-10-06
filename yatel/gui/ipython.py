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

_kernel_app = None
_manager = None
def _get_kernel_and_manager():

    global _kernel_app
    global _manager

    if _kernel_app is None:
        def _event_loop(kernel):
            kernel.timer = QtCore.QTimer()
            kernel.timer.timeout.connect(kernel.do_one_iteration)
            kernel.timer.start(1000 * kernel._poll_interval)

        _kernel_app = None
        _kernel_app = IPKernelApp.instance()
        _kernel_app.initialize(['python', '--pylab=qt'])
        _kernel_app.kernel.eventloop = _event_loop

        _connection_file = find_connection_file(_kernel_app.connection_file)
        _manager = QtKernelManager(connection_file=_connection_file)
        _manager.load_connection_file()
        _manager.start_channels()
        atexit.register(_manager.cleanup_connection_file)
        _kernel_app.start()
    return _kernel_app, _manager


#===============================================================================
# CLASS
#===============================================================================

class IPythonWidget(RichIPythonWidget):
    """IPython console connected to the default kernel embeddable in *Qt*.

    Note: This class is a singleton.

    """

    _instance = None # the singleton instance

    @staticmethod
    def __new__(cls, *args, **kwargs):
        """Only 1 instance

        """
        if not IPythonWidget._instance:
            instance = super(IPythonWidget, cls).__new__(cls)
            IPythonWidget._instance = instance
        return IPythonWidget._instance

    def __init__(self, welcome_message):
        """Return the instance of ``IPythonWidget``.

        """
        super(IPythonWidget, self).__init__(gui_completion='droplist')
        self._kernel_app, self.kernel_manager = _get_kernel_and_manager()
        self.write(welcome_message)

    def reset_ns(self, **kwargs):
        """Reset all commands and locals variables of the shell and setup anew
        vars on the namespace.

        **Params**
            :kwargs: Variables to be seted in the namespace.

        """
        self._kernel_app.shell.reset()
        self._kernel_app.shell.user_ns.update(kwargs)

    def write(self, msg):
        """Write the ``msg`` in the console."""
        self._kernel_app.shell.write(msg)

    def clear(self):
        """Reset all commands and locals variables of the shell and destroy
        this widget."""
        self._kernel_app.shell.reset()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
    app = QtGui.QApplication([''])
    widget = IPythonWidget("\n'k' is the kernel")
    widget.reset_ns(k=_kernel_app)
    widget.show()
    app.exec_()
