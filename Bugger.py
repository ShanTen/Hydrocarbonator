##############################################################
# Make-shift debug logger
##############################################################

class Bugger:
    def __init__(self,setState=None,notifyState=False):
        self.isActive = setState
        if notifyState == True: self.notifyState()

    def print(self, dbg_message):
        if self.isActive == True: 
            print(f"DBG OUT: {dbg_message}")

    def input(self,input_message, default_value=None):
        if self.isActive == False:
            return default_value
        if self.isActive == True: 
            return input(f"DBG IN: {input_message}")

    def log(self, dbg_message):
        if self.isActive == True: 
            print(f"DBG OUT: {dbg_message}")

    def activate(self):
        self.isActive = True

    def deactivate(self):
        self.isActive = False

    def notifyState(self):
        if self.isActive in [True, False]:
            print(f"DBG STATE: {self.isActive}")
            if self.isActive == False:
                print(f"All debug variables have been set to default values")
        else:
            print(f"Starting Debug State is undefined ({self.isActive}) which may not give desirable results.")