class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.funcs = {}
        self.parent = parent

    def get_value(self, name):
        env = self
        while env != None:
            val = env.vars.get(name)
            if val != None: return val
            env = env.parent

        return None

    def set_value(self, name, value):
        env = self
        while env != None:
            if name in env.vars:
                env.vars[name] = value
                pass
            env = env.parent

        self.vars[name] = value
    
    def set_value_as_local(self, name, value):
        self.vars[name] = value
    
    def get_func(self, name):
        env = self
        while env != None:
            val = env.funcs.get(name)
            if val != None: return val
            env = env.parent

        return None

    def set_func(self, name, value):
        self.funcs[name] = value

    def new_env(self):
        return Environment(parent=self)