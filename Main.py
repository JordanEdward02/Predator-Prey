# Main function that will run all of the experiments and create our findingsfrom playsound import playsound
import tkinter as tk
import Predator
import PreyZero
import PreyLocal
import PreyLocalEcho
import PreyGlobal
import Population  
import time
import pandas as pd

CANVAS_SIZE = 1000

MAXIMUM_PASSES = 6000
PASSES_NEEDED_FOR_VALIDITY = 2000

ZERO_COMMUNICATION = 0
LOCAL_COMMUNICATION = 1
LOCAL_ECHO_COMMUNICATION = 2
GLOBAL_COMMUNICATION = 3

def logicLoop(window, canvas, numberOfMoves, GlobalPrey, GlobalPred, preyType):
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
    if (numberOfMoves > PASSES_NEEDED_FOR_VALIDITY):
        frame = pd.DataFrame({"Prey": GlobalPrey, "Predators": GlobalPred})
        frame.to_excel("data.xlsx")
        window.destroy()
        return
    canvas.after(300,logicLoop, window, canvas, numberOfMoves, GlobalPrey, GlobalPred, preyType)

def renderlessLoop(experimentNumber, preyType):
    GlobalPrey = []
    GlobalPred = []
    numberOfMoves = 0
    pops = Population.Populations.getPopulations()
    while(numberOfMoves < MAXIMUM_PASSES and len(pops.allPred()) > 0 and len(pops.allPrey()) > 0):
        for pred in pops.allPred():
            pred.move()

        for prey in pops.allPrey():
            prey.move()
        
        if (preyType == LOCAL_COMMUNICATION or preyType == LOCAL_ECHO_COMMUNICATION):
            for prey in pops.allPrey():
                prey.clearComs()

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

def createCreatures(canvas, preyType):
    pops = Population.Populations.getPopulations()
    for i in range(20):
        pops.addPredator(Predator.Predator(canvas, "predator"))
    for i in range(60):
        if (preyType == ZERO_COMMUNICATION):
            pops.addPrey(PreyZero.Prey(canvas, "prey"))
        elif (preyType == LOCAL_COMMUNICATION):
            pops.addPrey(PreyLocal.Prey(canvas, "prey"))
        elif (preyType == LOCAL_ECHO_COMMUNICATION):
            pops.addPrey(PreyLocalEcho.Prey(canvas, "prey"))
        else:
            pops.addPrey(PreyGlobal.Prey(canvas, "prey"))
            

def main(rendered, numberOfExperiments, preyType):
    """
    Runs the experiements. If rendering, it will simply run a single parse, otherwise it will run numberOfExperiments times
    """
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    currentExperiment = [0]
    outputFrame = pd.DataFrame()
    if rendered:
        GlobalPrey = []
        GlobalPred = []
        window = tk.Tk()
        canvas = initialise(window)

        createCreatures(canvas, preyType)
        numberOfMoves = 0
        logicLoop(window, canvas, numberOfMoves, GlobalPrey, GlobalPred, preyType)

        window.mainloop()
    else:
        while (currentExperiment[0] < numberOfExperiments):
            createCreatures(None, preyType)
            findings = pd.DataFrame(renderlessLoop(currentExperiment, preyType))
            outputFrame = pd.concat([outputFrame, findings], axis=1)
        outputFrame.to_excel("data" + str(preyType) + ".xlsx")

main(rendered=True, numberOfExperiments=10, preyType=LOCAL_ECHO_COMMUNICATION)