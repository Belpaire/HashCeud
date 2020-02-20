class LibScans():
    def __init__(self,lib_id,booksnb,allbooks):
        self.lib_id=lib_id
        self.booksnb=booksnb
        self.allbooks=allbooks

class Result:
    def __init__(self,nlibs,LibScanslist):
        self.nblibs=nlibs
        self.LibScanslist=LibScanslist