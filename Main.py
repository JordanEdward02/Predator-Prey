# Main function that will run all of the experiments and create our findingsfrom playsound import playsound
import tkinter as tk
import Predator
import PreyZero

class Populations:
    def __init__(self,canvas):
        # Count the populations of the prey and predators as we run the simulation. Get these to be plot in real time.
        self.preyPop = 0
        self.predatorPop = 0
        self.canvas = canvas
        # Needs the item to count to be plotted on the graph
        
    def preyIncrement(self, canvas):
        self.preyPop += 1
        
    def preyDecrement(self, canvas):
        self.preyPop -= 1
        
    def predatorIncrement(self, canvas):
        self.predatorPop += 1
        
    def predatorDecrement(self, canvas):
        self.predatorPop -= 1
        
        

def logicLoop(canvas, predators, prey):

    for pred in predators:
        pred.draw()

    for p in prey:
        p.draw()
    canvas.after(50,logicLoop, canvas, predators, prey)

def initialise(window):
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=1000,height=1000)
    canvas.pack()
    return canvas

def createCreatures(canvas):
    
    predators = []
    for i in range(20):
        predators.append(Predator.Predator(canvas, "predator"))
        
    prey = []
    for i in range(100):
        prey.append(PreyZero.Prey(canvas, "prey"))
    return predators, prey

def main():
    window = tk.Tk()
    canvas = initialise(window)

    predators, prey = createCreatures(canvas)

    logicLoop(canvas, predators, prey)

    window.mainloop()
main()