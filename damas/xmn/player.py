class new:
    __action = lambda: None
    
    num     = 0
    name    = ''
    initial = ''
    
    def __init__(self, strategy, number, name):
        self.action = strategy
        self.num      = number
        self.name     = name
        self.initial  = name[0].lower()