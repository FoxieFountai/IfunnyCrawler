class Emitter():
    '''emission modules using (emitter name).on or (emitter name).emit'''
    def __init__(self):
        '''initialising emitter'''
        self.Functions = {}

    def on(self, functionname = None, function = None):
        if functionname == None or function == None:
            return

        if not functionname in self.Functions:
            self.Functions[functionname] = []
        
        self.Functions[functionname].append(function)
        return

    def emit(self, functionname = None, **kwargs):
        if functionname == None:
            return
        
        if functionname in self.Functions:
            for Func in self.Functions[functionname]:
                try:
                    Func(**kwargs)
                except:
                    print("Emitter named:" + str(functionname) + " >> there are many variables or some are missing.")

        else:
            return

def teste(id):
    print(str(id) + ' foi testado.')

if __name__ == '__main__':
    emission = Emitter()
    emission.on('print-a', lambda: print("a"))
    emission.on('test', teste)
    emission.emit('print-a')
    emission.emit('test', id=18818181)
