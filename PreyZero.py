# Model for the prey that have no  communication
import random
import math
import Population
from threading import Timer

WANDERING = 0
FLEEING = 1
REPRODUCING = 2

WALK_SPEED = 2
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
        self.reproduceDelay = random.randint(80,120)

    def move(self):
        pops = Population.Populations.getPopulations(self.canvas)

    
        # Reproduce counter always goes up
        self.reproduceTimer += 1
        if self.reproduceTimer == self.reproduceDelay: self.state = REPRODUCING

        if (self.state == FLEEING):
            if (len(pops.allPred()) == 0): return
            target = pops.allPred()[0]
            closestDist = 1000
            for pred in pops.allPred():
                if (self.distanceTo(pred) < closestDist):
                    target = pred
                    closestDist = self.distanceTo(pred)
            if (closestDist > 50):
                self.state = WANDERING
            else:
                ang = self.angleTo(target)
                if (abs(ang)<3.0):
                    if (ang > 0):
                        self.theta -= math.radians(ROTATION_SPEED)
                    else:
                        self.theta += math.radians(ROTATION_SPEED)
            self.theta = self.theta%(2.0*math.pi)
            self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))

        if (self.state == WANDERING):
            self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))
            self.theta += random.randint(-ROTATION_SPEED, ROTATION_SPEED) * math.pi/180
            for pred in pops.allPred():
                if (self.distanceTo(pred) < 30): 
                    self.state = FLEEING            
        
        self.collisions()
        if (self.state == REPRODUCING):
            self.reproduceCount += 1
            if self.reproduceCount > 10:
                newPrey = Prey(self.canvas, "prey")
                newPrey.setLocation(self.x+(8*math.cos(self.theta)), self.y+(8*math.sin(self.theta)))
                newPrey.theta = self.theta
                pops.addPrey(newPrey)
                self.reproduceTimer = 0
                self.reproduceCount = 0
                self.state = WANDERING

    def distanceTo(self, other):
        return math.sqrt( math.pow(self.x-other.x,2) + math.pow(self.y-other.y,2))
    
    def angleTo(self, other):
        # Find the angle from our current direction to the other object in radians. [-pi, pi]
        targetTheta = math.atan2(other.y - self.y, other.x - self.x)
        returnTheta = ((targetTheta - self.theta + math.pi) % (2.0*math.pi)) - math.pi
        return returnTheta
    
    def collisions(self):
        pops = Population.Populations.getPopulations(self.canvas)
        for prey in pops.allPrey():
            if prey == self:
                continue
            if self.distanceTo(prey) < 12:
                ang = math.atan2(prey.y - self.y, prey.x - self.x)
                self.setLocation(self.x-2*WALK_SPEED*math.cos(ang),self.y-2*WALK_SPEED*math.sin(ang))
                self.theta = (ang + math.pi)

    def draw(self):
        """
        canvas = self.canvas
        canvas.delete(self.name)
        # Body
        bounds = [ 
                   self.x-6,
                   self.y-6,
                   self.x+6,
                   self.y+6
        ]
        canvas.create_oval(bounds, fill="green", tags=self.name)

        # Head
        line_bounds = [
            self.x,
            self.y,
            self.x+9*math.cos(self.theta),
            self.y+9*math.sin(self.theta)
        ]
        canvas.create_line(line_bounds,fill="green",tags=self.name)
        """

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