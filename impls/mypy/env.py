class ENV():
    def __init__(self, outer=None, binds=None, exprs=None):
        self.data = {}
        self.outer= outer
        
        if binds:
            for k,v in zip(binds, exprs):
                self.data[k] = v
    
    def set(self, k, v):
        self.data[k]=v
        return v

    def get(self, k):
        env = self.find(k)
        if not env:
            raise Exception(f"{k} not found")
        return env.data[k]

    def find(self, k):
        if k in self.data:
            return self
        elif self.outer:
            return self.outer.find(k)
        else:
            return None