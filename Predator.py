# Model of the predators within our environment
import random
import math
import Population

HUNTING = 0
REPRODUCING = 1

WALK_SPEED = 3
ROTATION_SPEED = 5

class Predator():
    count = 0

    def __init__(self,canvas,name):
        self.x = random.randint(10,990)
        self.y = random.randint(10,990)
        self.theta = random.uniform(0.0,2.0*math.pi)
        self.energy = 100
        self.reproduceTimer = 0
        self.reproduceCount = 0
        self.canvas = canvas
        self.name = name + str(Predator.count)
        Predator.count += 1
        self.state = HUNTING
        self.view = [0]*9 # Are we having movmenet based on proximity or visibility?


    def move(self):
        self.energy -= 1
        if (self.energy<0):
            pops = Population.Populations.getPopulations(self.canvas)
            pops.destoryPredator(self)
            self.canvas.delete(self.name)
            return
        
        self.reproduceTimer += 1
        if self.reproduceTimer == 150:
            self.state = REPRODUCING
            return

        if (self.state == HUNTING):
            # Change this to move towards nearby prey
            self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))
            self.theta += random.randint(-ROTATION_SPEED, ROTATION_SPEED) * math.pi/180
            self.collisions()
            return
        
        if (self.state == REPRODUCING):
            self.reproduceCount += 1
            if self.reproduceCount > 10:
                pops = Population.Populations.getPopulations(self.canvas)
                newPred = Predator(self.canvas, "predator")
                newPred.setLocation(self.x+(4*random.randint(-1,1)), self.y+(4*random.randint(-1,1)))
                pops.addPredator(newPred)
                self.reproduceTimer = 0
                self.reproduceCount = 0
                self.state = HUNTING
            
                    
    def collisions(self):
        pops = Population.Populations.getPopulations(self.canvas)
        for prey in pops.allPrey():
            # Eat the prey if within range
            if self.distanceTo(prey) < 4:
                self.energy += 40
                if (self.energy > 100): self.energy = 100
                pops.destoryPrey(prey)
                prey.delete()
                return
        

    def distanceTo(self, other):
        return math.sqrt( math.pow(self.x-other.x,2) + math.pow(self.y-other.y,2))


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

        # Head
        line_bounds = [
            self.x,
            self.y,
            self.x+6*math.cos(self.theta),
            self.y+6*math.sin(self.theta)
        ]
        canvas.create_line(line_bounds,fill="red",tags=self.name)

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
