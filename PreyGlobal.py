# Model for the prey that have global communication

"""
Since this is much more of an unrealistic concept for the agents, we take it to the extreme.
Agents know where they are (which is not an unfair assumption since animals learn their surroundings)

They can then post their location to the blackboard when then see a predator 
Prey which are just wandering can then know the locations of all their fleeing comrade are move away from the closest  
"""
import random
import math
import Population

CANVAS_SIZE = 1000

WANDERING = 0
FLEEING = 1
REPRODUCING = 2

PERCEPTION_DISTANCE = 80

WALK_SPEED = 4
ROTATION_SPEED = 10

class Prey():
    count = 0

    blackboard = {}

    def __init__(self,canvas,name):
        self.x = random.randint(10,CANVAS_SIZE-10)
        self.y = random.randint(10,CANVAS_SIZE-10)
        self.theta = random.uniform(0.0,2.0*math.pi)
        self.reproduceTimer = 0
        self.canvas = canvas
        self.name = name + str(Prey.count)
        Prey.count += 1
        self.state = WANDERING
        self.reproduceCount = 0
        self.reproduceDelay = random.randint(160,200) - (40 - len(Population.Populations.getPopulations().allPrey())/10)

    def move(self):
        pops = Population.Populations.getPopulations()
    
        # Reproduce counter always goes up
        self.reproduceTimer += 1

        if self.reproduceTimer > self.reproduceDelay: 
            self.state = REPRODUCING

        """
        Here we post the alerts that our current prey is fleeing from a predator.
        We post the prey name (so we can remove it later) and the location
        """

        if (self.state == FLEEING):
            if (len(pops.allPred()) == 0): 
                return
            target = pops.allPred()[0]
            closestDist = 2000
            for pred in pops.allPred():
                if (self.distanceTo(pred) < closestDist):
                    target = pred
                    closestDist = self.distanceTo(pred)
            if (closestDist > PERCEPTION_DISTANCE):
                self.state = WANDERING
            else:
                ang = self.angleTo(target)
                if (abs(ang)<3.0):
                    if (ang > 0):
                        self.theta -= math.radians(ROTATION_SPEED)
                    else:
                        self.theta += math.radians(ROTATION_SPEED)
            Prey.blackboard[self.name] = [self.x, self.y] # Alerts that this prey has seen a predator
            self.theta = self.theta%(2.0*math.pi)
            self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))

        if (self.state == WANDERING):
            if (self.name in Prey.blackboard): Prey.blackboard.pop(self.name)
            """
            Here we find the nearest alert from another prey that is fleeing and move away from that. 
            We are assuming the closest alert is the most potentially dangerous to us, which is a fiar assumption
             and it works off the location of the prey since this is more realistic to be sharable between prey then the location of 
             the predator which we are evading
            """
            nearestAlertDistance = 1000.0
            nearestAlertLocation = [] 
            for alertLocation in Prey.blackboard.items():
                dist = math.sqrt( math.pow(self.x-alertLocation[1][0],2) + math.pow(self.y-alertLocation[1][1],2))
                if (dist < nearestAlertDistance):
                    nearestAlertLocation = alertLocation[1]
            if (nearestAlertLocation != []):
                targetTheta = math.atan2(nearestAlertLocation[1] - self.y, nearestAlertLocation[0] - self.x)
                relativeTheta = ((targetTheta - self.theta + math.pi) % (2.0*math.pi)) - math.pi
                if (abs(relativeTheta)<3.0):
                    if (relativeTheta > 0):
                        self.theta -= math.radians(ROTATION_SPEED)
                    else:
                        self.theta += math.radians(ROTATION_SPEED)
            else:
                self.theta += random.randint(-ROTATION_SPEED, ROTATION_SPEED) * math.pi/180
            self.theta = self.theta%(2.0*math.pi)
            self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))
            for allPred in pops.allPred():
                if (self.distanceTo(allPred) < PERCEPTION_DISTANCE):
                    self.state = FLEEING
                    break
            
            if (self.name in Prey.blackboard): Prey.blackboard.pop(self.name)
            

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
                self.reproduceDelay = random.randint(160,200) - len(Population.Populations.getPopulations().allPrey())/10
                self.state = WANDERING

    def distanceTo(self, other):
        return math.sqrt( math.pow(self.x-other.x,2) + math.pow(self.y-other.y,2))
    
    def angleTo(self, other):
        """
        Find the angle from our current direction to the other object in radians. [-pi, pi]
        """
        targetTheta = math.atan2(other.y - self.y, other.x - self.x)
        relativeTheta = ((targetTheta - self.theta + math.pi) % (2.0*math.pi)) - math.pi
        return relativeTheta
    
    def collisions(self):
        pops = Population.Populations.getPopulations()
        for prey in pops.allPrey():
            if prey == self:
                continue
            if self.distanceTo(prey) < 24:
                ang = math.atan2(prey.y - self.y, prey.x - self.x)
                self.setLocation(self.x-2*WALK_SPEED*math.cos(ang),self.y-2*WALK_SPEED*math.sin(ang))
                self.theta = (ang + math.pi)

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
        canvas.create_oval(bounds, fill="green", tags=self.name)

        # Head
        line_bounds = [
            self.x,
            self.y,
            self.x+16*math.cos(self.theta),
            self.y+16*math.sin(self.theta)
        ]
        canvas.create_line(line_bounds,fill="green",tags=self.name)

        if (self.name in Prey.blackboard):
            bounds = [ 
                    self.x-80,
                    self.y-80,
                    self.x+80,
                    self.y+80
            ]
            canvas.create_oval(bounds, width = "1", tags=self.name)
        

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

    def delete(self):
        if (self.name in Prey.blackboard): Prey.blackboard.pop(self.name)
        if (self.canvas != None): self.canvas.delete(self.name)