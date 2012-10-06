class Mock(object):
    def __init__(self, *args, **kwargs):
            pass

    def __call__(self, *args, **kwargs):
        return Mock()

    def __getattribute__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()

MOCK_MODULES = ("graph_tool", "PyQt4", "numpy",  "QtCore2", "QtGui", "sip")
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()
