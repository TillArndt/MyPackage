__author__ = 'tholen'

from PyQt4 import QtCore

class CmsRunPostProcTool(QtCore.QObject):
    """
    Base class for post processing tool.
    """

    # signals
    started  = QtCore.pyqtSignal(QtCore.QObject)
    finished = QtCore.pyqtSignal(QtCore.QObject)
    message  = QtCore.pyqtSignal(QtCore.QObject, str)


    def __init__(self):
        super(CmsRunPostProcTool, self).__init__()
        self.tool_enabled = True


    def start(self, process):
        """
        This method is called after process has run. It should be overwritten
        by its subclasses. In case all processes are finished, the argument
        will be a list of finished processes.

        Don't forget to emit started and finished form this method!
        """

        pass


class CmsRunPostProcessor(QtCore.QObject):
    """
    Toolchain for post processing. Add tools via add_tool(...). For execution,
    the start() method is called on the tool. The hole chain is executed, at
    the end of each process and once again, when all processes are finished.
    """

    def __init__(self):
        super(CmsRunPostProcessor, self).__init__()
        self.toolchain = []


    def add_tool(self, tool):
        self.toolchain.append(tool)


    def start(self, process = None):
        """
        All tools in tool chain are executed. The argument 'process' may also
        be of type list, when all processes are finished.
        """
        for tool in self.toolchain:
            if tool.tool_enabled:
                tool.start(process)
