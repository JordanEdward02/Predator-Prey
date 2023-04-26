# Main function that will run all of the experiments and create our findingsfrom playsound import playsound
import tkinter as tk
import Predator
import PreyZero   
import Population  
import pandas as pd

CANVAS_SIZE = 1000

MAXIMUM_PASSES = 6000
PASSES_NEEDED_FOR_VALIDITY = 4000

def logicLoop(window, canvas, numberOfMoves):
    GlobalPrey = []
    GlobalPred = []
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
        window.destroy()
        return
    canvas.after(1,logicLoop, window, canvas, numberOfMoves)

def renderlessLoop(experimentNumber):
    GlobalPrey = []
    GlobalPred = []
    numberOfMoves = 0
    pops = Population.Populations.getPopulations()
    while(numberOfMoves < MAXIMUM_PASSES and len(pops.allPred()) > 0 and len(pops.allPrey()) > 0):
        for pred in pops.allPred():
            pred.move()

        for prey in pops.allPrey():
            prey.move()

        GlobalPrey.append(len(pops.allPrey()))
        GlobalPred.append(len(pops.allPred()))

        numberOfMoves += 1
    if numberOfMoves > PASSES_NEEDED_FOR_VALIDITY:
        print("Finished experiment: " + str(experimentNumber[0]))
        experimentNumber[0] += 1
        return {"Prey" + str(experimentNumber): GlobalPrey, "Predators" + str(experimentNumber): GlobalPred}

def initialise(window):
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=CANVAS_SIZE,height=CANVAS_SIZE)
    canvas.pack()
    return canvas

def createCreatures(canvas):
    pops = Population.Populations.getPopulations()
    for i in range(10):
        pops.addPredator(Predator.Predator(canvas, "predator"))
    for i in range(40):
        pops.addPrey(PreyZero.Prey(canvas, "prey"))

def main(rendered, numberOfExperiments):
    """
    Runs the experiements. If rendering, it will simply run a single parse, otherwise it will run numberOfExperiments times
    """
    currentExperiment = [0]
    outputFrame = pd.DataFrame()
    if rendered:
        window = tk.Tk()
        canvas = initialise(window)

        createCreatures(canvas)
        numberOfMoves = 0
        logicLoop(window, canvas, numberOfMoves)

        window.mainloop()
    else:
        while (currentExperiment[0] < numberOfExperiments):
            createCreatures(None)
            findings = pd.DataFrame(renderlessLoop(currentExperiment))
            outputFrame = pd.concat([outputFrame, findings], axis=1)
        outputFrame.to_excel("data.xlsx")

main(rendered=False, numberOfExperiments=5)