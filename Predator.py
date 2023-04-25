# Model of the predators within our environment
import random
import math

class Predator():
    count = 0

    def __init__(self,canvas,name):
        self.x = random.randint(10,990)
        self.y = random.randint(10,990)
        self.theta = random.uniform(0.0,2.0*math.pi)
        self.energy = 100
        self.canvas = canvas
        self.name = name + str(Predator.count)
        Predator.count += 1
        self.view = [0]*9 # Are we having movmenet based on proximity or visibility?

        
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
        canvas.create_oval(bounds, fill="red", tags=self.name)

        line_bounds = [
            self.x,
            self.y,
            self.x+6*math.cos(self.theta),
            self.y+6*math.sin(self.theta)
        ]
        canvas.create_line(line_bounds,fill="red",tags=self.name)
