# Class to maintain the populations over time of the predators and prey

class Populations():
    this = None    
    def __init__(self):
        # Count the populations of the prey and predators as we run the simulation. Get these to be plot in real time.
        self.preyPop = []
        self.predatorPop = []

        
    def getPopulations():
        if Populations.this == None:
            Populations.this = Populations()
        return Populations.this
        
    def destoryPrey(self, prey):
        self.preyPop.remove(prey)
        
    def addPrey(self, prey):
        self.preyPop.append(prey)
        
    def destoryPredator(self, pred):
        self.predatorPop.remove(pred)
        
    def addPredator(self, pred):
        self.predatorPop.append(pred)

    def allPred(self):
        return self.predatorPop
    
    def allPrey(self):
        return self.preyPop
    
    def reset(self):
        self.preyPop = []
        self.predatorPop = []
   