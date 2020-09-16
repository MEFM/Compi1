
class transicion:

    def __init__(self, eIni, tran, eFin):
        self.eIni = eIni
        self.tran = tran
        self.eFin = eFin
    
    def comp(self, eIni, tran):
        if (self.eIni == eIni) and (self.tran == tran):
            return True

        return False
    


    def string(self):
        return self.eIni+" "+self.tran+" "+self.eFin
    
    