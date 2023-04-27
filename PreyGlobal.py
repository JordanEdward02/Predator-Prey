# Model for the prey that have global communication


"""
Need a new idea for mapping this blackboard because this is exactly the same as the echoing local in theory.

Otherwise we can just say locations with their message in the blackboard? 
Not very realistic from a biological standpoint since creatures don't know where they are like that.
Maybe we could justify it if creatures know where they are based on local landmarks?? I guess find a reference for if
animals are aware of their surroundings.
"""
import random
import math
import Population

CANVAS_SIZE = 1000

WANDERING = 0
FLEEING = 1
REPRODUCING = 2

NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

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
        We post alerts to our blackboard here based on the connections between our prey and any nearby agents.
        These are triples using the python dictionary
        "currentPrey" : [[Direction, otherAgent], [Direction, otherAgent], ... []]
        
        should be interpreted as [currentPrey, Direction, OtherAgent]
        Dictionary is just used to keep it organised and quick

        When an agent comes to add new parts to this dictionary, we clear it because we don't want all the old alerts to be present
        """
        Prey.blackboard[self] = []

        for otherPrey in pops.allPrey():
            if otherPrey == self:
                continue
            if (self.distanceTo(otherPrey) < PERCEPTION_DISTANCE):
                targetTheta = math.atan2(otherPrey.y - self.y, otherPrey.x - self.x)
                if (abs(targetTheta) > (3.0*math.pi)/2): 
                    Prey.blackboard[self].append([EAST, otherPrey]) # For the direction, we use the opposite since it is to be intepreted by the reciever
                elif(targetTheta > math.pi/2):
                    Prey.blackboard[self].append([NORTH, otherPrey])
                elif(targetTheta < -math.pi/2):
                    Prey.blackboard[self].append([SOUTH, otherPrey])
                else:
                    Prey.blackboard[self].append([WEST, otherPrey])
        for otherPred in pops.allPred():
            if (self.distanceTo(otherPred) < PERCEPTION_DISTANCE):
                targetTheta = math.atan2(otherPred.y - self.y, otherPred.x - self.x)
                if (abs(targetTheta) > (3.0*math.pi)/2): 
                    Prey.blackboard[self].append([EAST, otherPred])
                elif(targetTheta > math.pi/2):
                    Prey.blackboard[self].append([NORTH, otherPred])
                elif(targetTheta < -math.pi/2):
                    Prey.blackboard[self].append([SOUTH, otherPred])
                else:
                    Prey.blackboard[self].append([WEST, otherPred])

        """
        Here we need to trace our knowledge graph
        """
        #print(Prey.blackboard[self])

        if (self.state == FLEEING):
            if (len(pops.allPred()) == 0): 
                return
            target = pops.allPred()[0]
            closestDist = 1000
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
            self.theta = self.theta%(2.0*math.pi)
            self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))

        if (self.state == WANDERING):
            for pred in pops.allPred():
                if (self.distanceTo(pred) < PERCEPTION_DISTANCE): 
                    self.state = FLEEING
            self.theta += random.randint(-ROTATION_SPEED, ROTATION_SPEED) * math.pi/180
            self.theta = self.theta%(2.0*math.pi)
            self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))

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
        if (self in Prey.blackboard): Prey.blackboard.pop(self)
        if (self.canvas != None): self.canvas.delete(self.name)