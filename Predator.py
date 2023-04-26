# Model of the predators within our environment
import random
import math
import Population

HUNTING = 0
REPRODUCING = 1
RECOVERY = 2

WALK_SPEED = 3
ROTATION_SPEED = 3

class Predator():
    count = 0

    def __init__(self,canvas,name):
        self.x = random.randint(10,990)
        self.y = random.randint(10,990)
        self.theta = random.uniform(0.0,2.0*math.pi)
        self.energy = 200
        self.reproduceCount = 0
        self.canvas = canvas
        self.name = name + str(Predator.count)
        Predator.count += 1
        self.state = HUNTING


    def move(self):
        pops = Population.Populations.getPopulations(self.canvas)

        self.energy -= 1
        if (self.energy<0):
            pops.destoryPredator(self)
            self.canvas.delete(self.name)
            return
        
        if (self.state == RECOVERY):
            self.preyCount += 1
            if self.preyCount > 10:
                self.state = HUNTING

        if (self.state == HUNTING):
            if self.energy > 500:
                self.state = REPRODUCING
                return
            
            # Find the nearest prey and move towards it
            if (len(pops.allPrey()) == 0): return
            target = pops.allPrey()[0]
            closestDist = 1000
            for prey in pops.allPrey():
                if (self.distanceTo(prey) < closestDist):
                    target = prey
                    closestDist = self.distanceTo(prey)
            if (closestDist > 50):
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
                newPred.setLocation(self.x+(12*math.cos(self.theta)), self.y+(12*math.sin(self.theta)))
                newPred.theta = self.theta
                pops.addPredator(newPred)
                self.reproduceCount = 0
                self.state = HUNTING
                self.energy = 200
            
                    
    def collisions(self):
        pops = Population.Populations.getPopulations(self.canvas)
        for prey in pops.allPrey():
            # Eat the prey if within range
            if self.distanceTo(prey) < 10:
                self.energy += 60
                pops.destoryPrey(prey)
                prey.delete()
                return
        for pred in pops.allPred():
            if pred == self:
                continue
            if self.distanceTo(pred) < 14:
                ang = self.angleTo(prey)
                self.setLocation(self.x-WALK_SPEED*math.cos(ang),self.y-WALK_SPEED*math.sin(ang))
        

    def distanceTo(self, other):
        return math.sqrt( math.pow(self.x-other.x,2) + math.pow(self.y-other.y,2))
    
    def angleTo(self, other):
        # Find the angle from our current direction to the other object in radians. [-pi, pi]
        targetTheta = math.atan2(other.y - self.y, other.x - self.x)
        returnTheta = ((targetTheta - self.theta + math.pi) % (2.0*math.pi)) - math.pi
        return returnTheta


    def draw(self):
        """
        canvas = self.canvas
        canvas.delete(self.name)
        # Body
        bounds = [ 
                   self.x-8,
                   self.y-8,
                   self.x+8,
                   self.y+8
        ]
        canvas.create_oval(bounds, fill="red", tags=self.name)

        # Head
        line_bounds = [
            self.x,
            self.y,
            self.x+12*math.cos(self.theta),
            self.y+12*math.sin(self.theta)
        ]
        canvas.create_line(line_bounds,fill="red",tags=self.name)
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
