# Model for the prey that have no  communication
import random
import math
import Population
from threading import Timer

WANDERING = 0
FLEEING = 1
REPRODUCING = 2

WALK_SPEED = 3
ROTATION_SPEED = 5

class Prey():
    count = 0

    def __init__(self,canvas,name):
        self.x = random.randint(10,990)
        self.y = random.randint(10,990)
        self.theta = random.uniform(0.0,2.0*math.pi)
        self.reproduceTimer = 0
        self.canvas = canvas
        self.name = name + str(Prey.count)
        Prey.count += 1
        self.state = WANDERING
        self.reproduceCount = 0
        self.view = [0]*9 # Are we having movmenet based on proximity or visibility?

        

    def move(self):
        # Reproduce counter always goes up
        self.reproduceTimer += 1
        if self.reproduceTimer == 100:
            self.state = REPRODUCING
            return

        if (self.state == WANDERING):
            self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))
            self.theta += random.randint(-ROTATION_SPEED, ROTATION_SPEED) * math.pi/180
            return
        
        if (self.state == REPRODUCING):
            self.reproduceCount += 1
            if self.reproduceCount > 10:
                pops = Population.Populations.getPopulations(self.canvas)
                newPrey = Prey(self.canvas, "prey")
                newPrey.setLocation(self.x+(4*random.randint(-1,1)), self.y+(4*random.randint(-1,1)))
                pops.addPrey(newPrey)
                self.reproduceTimer = 0
                self.reproduceCount = 0
                self.state = WANDERING


    def draw(self):
        canvas = self.canvas
        canvas.delete(self.name)
        # Body
        bounds = [ 
                   self.x-2,
                   self.y-2,
                   self.x+2,
                   self.y+2
        ]
        canvas.create_oval(bounds, fill="green", tags=self.name)

        # Head
        line_bounds = [
            self.x,
            self.y,
            self.x+6*math.cos(self.theta),
            self.y+6*math.sin(self.theta)
        ]
        canvas.create_line(line_bounds,fill="green",tags=self.name)

    def setLocation(self, x, y):
        if (x > 1000):
            x -= 1000
        if (x<0):
            x += 1000
        if (y > 1000):
            y -= 1000
        if (y<0):
            y += 1000
        self.x = x
        self.y = y

    def delete(self):
        self.canvas.delete(self.name)