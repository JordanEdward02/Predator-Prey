# Main function that will run all of the experiments and create our findingsfrom playsound import playsound
import tkinter as tk
import Predator
import PreyZero   
import Population  

def logicLoop(canvas):
    # Main logic loop that renders every object. Objects draw themselves so once we remove the graphics, do this in their classes.
    pops = Population.Populations.getPopulations(canvas)
    for pred in pops.allPred():
        pred.move()

    for prey in pops.allPrey():
        prey.move()

    for pred in pops.allPred():
        pred.draw()

    for p in pops.allPrey():
        p.draw()
    canvas.after(50,logicLoop, canvas)

def initialise(window):
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=1000,height=1000)
    canvas.pack()
    return canvas

def createCreatures(canvas):
    pops = Population.Populations.getPopulations(canvas)
    for i in range(20):
        pops.addPredator(Predator.Predator(canvas, "predator"))
        
    for i in range(100):
        pops.addPrey(PreyZero.Prey(canvas, "prey"))

def main():
    window = tk.Tk()
    canvas = initialise(window)

    pops = createCreatures(canvas)
    logicLoop(canvas)

    window.mainloop()
main()