class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get_value(self, name):
        env = self
        while env != None:
            val = env.vars.get(name)
            if val != None: return val
            env = env.parent
        return None

    def set_vale(self, name, value):
        env = self
        while env != None:
            if name in env.vars:
                env.vars[name] = value
                return env.vars[name]
            env = env.parent
        self.vars[name] = value
        return self.vars[name]

    def new_env(self):
        return Environment(parent=self)