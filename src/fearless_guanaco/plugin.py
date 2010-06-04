
PT_METRIC_PLUGIN = "metric_plugin"

PLUGINS_TYPES = [PT_METRIC_PLUGIN]

class AbstractPlugin(object):
    
    def __init__(self):
        self.setup()

    def __del__(self):
        self.teardown()
    
    def get_plugin_type(self):
        raise NotImplementedError()
        
    def setup(self):
        raise NotImplementedError()
    
    def teardown(self):
        raise NotImplementedError()
    
    def task(self):
        raise NotImplementedError()
    
    def has_gui(self):
        raise NotImplementedError()
    
    def get_gui(self):
        raise NotImplementedError()
               

def get_plugins(plugin_paths):
    plugins = {}
    for k in PLUGINS_TYPES:
        plugins[k] = []
    return plugin
