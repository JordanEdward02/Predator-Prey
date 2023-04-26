# Main function that will run all of the experiments and create our findingsfrom playsound import playsound
import tkinter as tk
import Predator
import PreyZero   
import Population  
import pandas as pd

GlobalPrey = []
GlobalPred = []

def logicLoop(window, canvas, numberOfMoves):
    # Main logic loop that renders every object. Objects draw themselves so once we remove the graphics, do this in their classes.
    pops = Population.Populations.getPopulations()
    for pred in pops.allPred():
        pred.move()

    for prey in pops.allPrey():
        prey.move()

    for pred in pops.allPred():
        pred.draw()

    for p in pops.allPrey():
        p.draw()
    
    GlobalPrey.append(len(pops.allPrey()))
    GlobalPred.append(len(pops.allPred()))
    if len(pops.allPred()) == 0 or len(pops.allPrey()) == 0:
        frame = pd.DataFrame({"Prey": GlobalPrey, "Predators": GlobalPred})
        frame.to_excel("data.xlsx")
        window.destroy()
        return

    numberOfMoves += 1
    if (numberOfMoves > 3000):
        frame = pd.DataFrame({"Prey": GlobalPrey, "Predators": GlobalPred})
        frame.to_excel("data.xlsx")
        window.destroy()
        return
    canvas.after(1,logicLoop, window, canvas, numberOfMoves)

def renderlessLoop(numberOfMoves):
    pops = Population.Populations.getPopulations()
    while(numberOfMoves < 3000 and len(pops.allPred()) > 0 and len(pops.allPrey()) > 0):
        for pred in pops.allPred():
            pred.move()

        for prey in pops.allPrey():
            prey.move()

        GlobalPrey.append(len(pops.allPrey()))
        GlobalPred.append(len(pops.allPred()))

        print(str(len(pops.allPrey())) + " || " + str(len(pops.allPred())))
        numberOfMoves += 1
    frame = pd.DataFrame({"Prey": GlobalPrey, "Predators": GlobalPred})
    frame.to_excel("data.xlsx")

def initialise(window):
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=1000,height=1000)
    canvas.pack()
    return canvas

def createCreatures(canvas):
    pops = Population.Populations.getPopulations()
    for i in range(30):
        pops.addPredator(Predator.Predator(canvas, "predator"))
    for i in range(500):
        pops.addPrey(PreyZero.Prey(canvas, "prey"))

def main(rendered):
    if rendered:
        window = tk.Tk()
        canvas = initialise(window)

        createCreatures(canvas)
        numberOfMoves = 0
        logicLoop(window, canvas, numberOfMoves)

        window.mainloop()
    else:
        createCreatures(None)
        numberOfMoves = 0
        renderlessLoop(numberOfMoves)

main(rendered=False)