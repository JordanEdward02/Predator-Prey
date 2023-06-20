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
import random
import math

CANVAS_SIZE = 1000

MAXIMUM_PASSES = 6000
PASSES_NEEDED_FOR_VALIDITY = 4000

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
    canvas.after(1,logicLoop, window, canvas, numberOfMoves, GlobalPrey, GlobalPred, preyType)

def renderlessLoop(experimentNumber, preyType):
    """
    Runs a single pass of the simulation with the specified prey type
    """
    GlobalPrey = []
    GlobalPred = []
    numberOfMoves = 0
    #print("TYPE: " + str(preyType))
    pops = Population.Populations.getPopulations()
    while(numberOfMoves < MAXIMUM_PASSES and len(pops.allPred()) > 0 and len(pops.allPrey()) > 0):
        for pred in pops.allPred():
            pred.move()

        for prey in pops.allPrey():
            prey.move()

        GlobalPrey.append(len(pops.allPrey()))
        GlobalPred.append(len(pops.allPred()))

        numberOfMoves += 1
    agentCounts = pd.DataFrame({"Prey"+str(preyType): len(pops.allPrey()), "Predator"+str(preyType): len(pops.allPred())}, index = [0])
    if numberOfMoves > PASSES_NEEDED_FOR_VALIDITY:
        print("Successful experiment: " + str(experimentNumber[0]))
        experimentNumber[0] += 1
        return {"Prey" + str(experimentNumber): GlobalPrey, "Predators" + str(experimentNumber): GlobalPred}, agentCounts
    return None, agentCounts

def initialise(window):
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=CANVAS_SIZE,height=CANVAS_SIZE)
    canvas.pack()
    return canvas

def createCreatures(canvas, preyType):
    """
    Creates the creatures in Population.py 
    """
    pops = Population.Populations.getPopulations()
    pops.reset()
    for _ in range(20):
        x = random.randint(10, CANVAS_SIZE-10)
        y = random.randint(10, CANVAS_SIZE-10)
        theta = random.uniform(0.0,2.0*math.pi)
        pops.addPredator(Predator.Predator(canvas, "predator", x, y, theta))
    for _ in range(60):
        x = random.randint(10, CANVAS_SIZE-10)
        y = random.randint(10, CANVAS_SIZE-10)
        theta = random.uniform(0.0,2.0*math.pi)
        if (preyType == ZERO_COMMUNICATION):
            pops.addPrey(PreyZero.Prey(canvas, "prey",x,y,theta))
        elif (preyType == LOCAL_COMMUNICATION):
            pops.addPrey(PreyLocal.Prey(canvas, "prey",x,y,theta))
        elif (preyType == LOCAL_ECHO_COMMUNICATION):
            pops.addPrey(PreyLocalEcho.Prey(canvas, "prey",x,y,theta))
        else:
            pops.addPrey(PreyGlobal.Prey(canvas, "prey",x,y,theta))
            

def main(rendered, numberOfExperiments):
    """
    Runs the experiements. If rendering, it will simply run a single parse, otherwise it will run numberOfExperiments times
    """
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    currentExperiment = [0]
    attemptNumber = 0

    if rendered:
        GlobalPrey = []
        GlobalPred = []
        window = tk.Tk()
        canvas = initialise(window)

        createCreatures(canvas, LOCAL_ECHO_COMMUNICATION)
        numberOfMoves = 0
        logicLoop(window, canvas, numberOfMoves, GlobalPrey, GlobalPred, LOCAL_ECHO_COMMUNICATION)

        window.mainloop()
    else:
        outputFrameZero = pd.DataFrame()
        outputFrameLocal = pd.DataFrame()
        outputFrameLocalEcho = pd.DataFrame()
        outputFrameGlobal = pd.DataFrame()

        zeroagentCounts = pd.DataFrame()
        localagentCounts = pd.DataFrame()
        localEchoagentCounts = pd.DataFrame()
        globalagentCounts = pd.DataFrame()
        while (attemptNumber < numberOfExperiments):
            """
            Uses the same seed in all 4 experiments so we can accurately conclude how the behaviour impacts the populations and stability
            rather than variations in the spawning data impacts it
            """
            seed = time.time()
            for preyType in range(4):
                random.seed(seed)
                createCreatures(None, preyType)
                """
                Stores the data in the correct place based on the prey type
                """
                findings, agentCounts = renderlessLoop(currentExperiment, preyType)
                if (findings != None):
                    if (preyType == ZERO_COMMUNICATION):
                        outputFrameZero = pd.concat([outputFrameZero, pd.DataFrame(findings)], axis=1)
                    if (preyType == LOCAL_COMMUNICATION):
                        outputFrameLocal = pd.concat([outputFrameLocal, pd.DataFrame(findings)], axis=1)
                    if (preyType == LOCAL_ECHO_COMMUNICATION):
                        outputFrameLocalEcho = pd.concat([outputFrameLocalEcho, pd.DataFrame(findings)], axis=1)
                    if (preyType == GLOBAL_COMMUNICATION):
                        outputFrameGlobal = pd.concat([outputFrameGlobal, pd.DataFrame(findings)], axis=1)
                
                if (preyType == ZERO_COMMUNICATION):
                    zeroagentCounts = pd.concat([zeroagentCounts, agentCounts])
                if (preyType == LOCAL_COMMUNICATION):
                    localagentCounts = pd.concat([localagentCounts, agentCounts])
                if (preyType == LOCAL_ECHO_COMMUNICATION):
                    localEchoagentCounts = pd.concat([localEchoagentCounts, agentCounts])
                if (preyType == GLOBAL_COMMUNICATION):
                    globalagentCounts = pd.concat([globalagentCounts, agentCounts])
            attemptNumber += 1
            print(str(attemptNumber))
        outputFrameZero.to_excel("stableZero.xlsx")
        outputFrameLocal.to_excel("stableLocal.xlsx")
        outputFrameLocalEcho.to_excel("stableLocalEcho.xlsx")
        outputFrameGlobal.to_excel("stableGlobal.xlsx")

        endingPopulations = pd.concat([zeroagentCounts, localagentCounts, localEchoagentCounts, globalagentCounts], axis=1)
        endingPopulations.to_excel("endingPopulations.xlsx")
        
        print("COLUMNS(): " + str(outputFrameLocal.columns.size/2))

main(rendered=False, numberOfExperiments=300)