# Model of the predators within our environment
import random
import math
import Population

CANVAS_SIZE = 1000

HUNTING = 0
REPRODUCING = 1
RECOVERY = 2

WALK_SPEED = 6
ROTATION_SPEED = 10

class Predator():
    count = 0

    def __init__(self,canvas,name, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.energy = random.randint(70,130) + 60 - len(Population.Populations.getPopulations().allPred())*3
        self.canvas = canvas
        self.name = name + str(Predator.count)
        Predator.count += 1
        self.state = HUNTING


    def move(self):
        pops = Population.Populations.getPopulations()

        self.energy -= 1
        if (self.energy<0):
            pops.destoryPredator(self)
            if (self.canvas != None): self.canvas.delete(self.name)
            return
        
        if (self.state == RECOVERY):
            self.preyCount += 1
            if self.preyCount > 10:
                self.state = HUNTING

        if (self.state == HUNTING):
            if self.energy > 200:
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
            if (closestDist > 60):
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
            pops = Population.Populations.getPopulations()
            newPred = Predator(self.canvas, "predator", self.x+(24*math.cos(self.theta)), self.y+(24*math.sin(self.theta)), self.theta)
            pops.addPredator(newPred)
            self.state = HUNTING
            self.energy = random.randint(70,130) + 60 - len(Population.Populations.getPopulations().allPred())*3
            
                    
    def collisions(self):
        pops = Population.Populations.getPopulations()
        for prey in pops.allPrey():
            # Eat the prey if within range
            if self.distanceTo(prey) < 24:
                self.energy += random.randint(30,50) + 60 - len(Population.Populations.getPopulations().allPred())*3
                pops.destoryPrey(prey)
                prey.delete()
                return
        for pred in pops.allPred():
            if pred == self:
                continue
            if self.distanceTo(pred) < 24:
                ang = math.atan2(pred.y - self.y, pred.x - self.x)
                self.setLocation(self.x-WALK_SPEED*math.cos(ang),self.y-WALK_SPEED*math.sin(ang))
                self.theta = ang+math.pi
        

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
                   self.x-12,
                   self.y-12,
                   self.x+12,
                   self.y+12
        ]
        canvas.create_oval(bounds, fill="red", tags=self.name)

        # Head
        line_bounds = [
            self.x,
            self.y,
            self.x+16*math.cos(self.theta),
            self.y+16*math.sin(self.theta)
        ]
        canvas.create_line(line_bounds,fill="red",tags=self.name)
        

    def setLocation(self, x, y):
        if (x > CANVAS_SIZE):
            x -= CANVAS_SIZE
        if (x<0):
            x += CANVAS_SIZE
        if (y > CANVAS_SIZE):
            y -= CANVAS_SIZE
        if (y<0):
            y += CANVAS_SIZE
        self.x = x
        self.y = y
