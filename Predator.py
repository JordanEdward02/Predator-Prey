# Model of the predators within our environment
import random
import math
import Population

HUNTING = 0
REPRODUCING = 1

WALK_SPEED = 4
ROTATION_SPEED = 8

class Predator():
    count = 0

    def __init__(self,canvas,name):
        self.x = random.randint(10,990)
        self.y = random.randint(10,990)
        self.theta = random.uniform(0.0,2.0*math.pi)
        self.energy = 100
        self.reproduceCount = 0
        self.canvas = canvas
        self.name = name + str(Predator.count)
        Predator.count += 1
        self.state = HUNTING
        self.view = [0]*9 # Are we having movmenet based on proximity or visibility?


    def move(self):
        pops = Population.Populations.getPopulations(self.canvas)
        if (self.state == HUNTING):
            if self.energy > 200 :
                self.state = REPRODUCING
                return
            self.energy -= 1
            if (self.energy<0):
                pops.destoryPredator(self)
                self.canvas.delete(self.name)
                return
            # Change this to move towards nearby prey
            target = pops.allPrey()[0]
            closestDist = 1000
            for prey in pops.allPrey():
                if (self.distanceTo(prey) < closestDist):
                    target = prey
                    closestDist = self.distanceTo(prey)
            if (closestDist > 40):
                self.theta += math.radians(random.randint(-ROTATION_SPEED, ROTATION_SPEED))
            else:
                ang = self.angleTo(target)
                if (abs(ang)>0.1):
                    if (ang > 0):
                        self.theta += math.radians(ROTATION_SPEED)
                    else:
                        self.theta -= math.radians(ROTATION_SPEED)
            self.theta = self.theta%(2.0*math.pi)
            self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))
            self.collisions()
            return
        
        if (self.state == REPRODUCING):
            self.reproduceCount += 1
            if self.reproduceCount > 10:
                pops = Population.Populations.getPopulations(self.canvas)
                newPred = Predator(self.canvas, "predator")
                newPred.setLocation(self.x+(4*random.randint(-1,1)), self.y+(4*random.randint(-1,1)))
                pops.addPredator(newPred)
                self.reproduceCount = 0
                self.state = HUNTING
                if self.energy >200: self.energy = 100
            
                    
    def collisions(self):
        pops = Population.Populations.getPopulations(self.canvas)
        for prey in pops.allPrey():
            # Eat the prey if within range
            if self.distanceTo(prey) < 4:
                self.energy += 65
                pops.destoryPrey(prey)
                prey.delete()
                return
        

    def distanceTo(self, other):
        return math.sqrt( math.pow(self.x-other.x,2) + math.pow(self.y-other.y,2))
    
    def angleTo(self, other):
        # Find the angle from our current direction to the other object in radians. [-pi, pi]
        targetTheta = math.atan2(other.y - self.y, other.x - self.x)
        returnTheta = ((targetTheta - self.theta + math.pi) % (2.0*math.pi)) - math.pi
        return returnTheta


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
