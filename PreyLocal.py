# Model for the prey that have local communication
import random
import math
import Population

CANVAS_SIZE = 1000

WANDERING = 0
FLEEING = 1
REPRODUCING = 2

NORTH = -1
SOUTH = 1

EAST = 1
WEST = -1

PERCEPTION_DISTANCE = 80

WALK_SPEED = 4
ROTATION_SPEED = 10

class Prey():
    count = 0

    def __init__(self,canvas,name, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.reproduceTimer = 0
        self.canvas = canvas
        self.name = name + str(Prey.count)
        Prey.count += 1
        self.state = WANDERING
        self.reproduceCount = 0
        self.reproduceDelay = random.randint(160,200) - (40 - len(Population.Populations.getPopulations().allPrey())/10)
        self.coms = []

    def move(self):
        pops = Population.Populations.getPopulations()

    
        # Reproduce counter always goes up
        self.reproduceTimer += 1
        if self.reproduceTimer > self.reproduceDelay: self.state = REPRODUCING

        if (self.state == FLEEING):
            if (len(pops.allPred()) == 0): return
            target = pops.allPred()[0]
            closestDist = 1000
            for pred in pops.allPred():
                if (self.distanceTo(pred) < closestDist):
                    target = pred
                    closestDist = self.distanceTo(pred)
            if (closestDist > 80):
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
            
            """
            This is our sending out of the communication. Doesn't use a full triple since this doesn't repeat through 
            the prey, it just occurs once and any near enough hear.
            """
            for otherPrey in pops.allPrey():
                if otherPrey == self:
                    continue
                if (self.distanceTo(otherPrey) < PERCEPTION_DISTANCE):
                    targetTheta = math.atan2(otherPrey.y - self.y, otherPrey.x - self.x)
                    if (abs(targetTheta) > (3.0*math.pi)/2):
                        otherPrey.alert([EAST, 0]) # For the direction, we use the opposite since it is to be intepreted by the reciever
                    elif(targetTheta > math.pi/2):
                        otherPrey.alert([0,NORTH])
                    elif(targetTheta < -math.pi/2):
                        otherPrey.alert([0,SOUTH])
                    else:
                        otherPrey.alert([WEST, 0])

        if (self.state == WANDERING):
            for pred in pops.allPred():
                if (self.distanceTo(pred) < PERCEPTION_DISTANCE): 
                    self.state = FLEEING         
            if (self.state == WANDERING):
                if (len(self.coms) > 0):
                    """
                    Communication for this localised version all have the same presedence since we are looking at most
                    at a difference of 1 prey. 
                    Therefore we find  the average and move away from that.
                    Alternatively we could just move away from any random one.s
                    """
                    averageDir = [0,0]
                    for com in self.coms:
                        averageDir = [averageDir[0] + com[0], averageDir[1] + com[1]]
                    oppositeTheta = math.atan2(averageDir[0], averageDir[1])
                    relativeTheta = ((oppositeTheta - self.theta + math.pi) % (2.0*math.pi)) - math.pi
                    if (abs(relativeTheta)<3.0):
                        if (relativeTheta > 0):
                            self.theta -= math.radians(ROTATION_SPEED)
                        else:
                            self.theta += math.radians(ROTATION_SPEED)
                            
                    self.theta = self.theta%(2.0*math.pi)
                    self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))

                else:
                    self.theta += random.randint(-ROTATION_SPEED, ROTATION_SPEED) * math.pi/180
                    self.theta = self.theta%(2.0*math.pi)
                    self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))
            else:
                    self.theta += random.randint(-ROTATION_SPEED, ROTATION_SPEED) * math.pi/180
                    self.theta = self.theta%(2.0*math.pi)
                    self.setLocation(self.x+WALK_SPEED*math.cos(self.theta),self.y+WALK_SPEED*math.sin(self.theta))
        self.collisions()
        if (self.state == REPRODUCING):
            self.reproduceCount += 1
            if self.reproduceCount > 10:
                newPrey = Prey(self.canvas, "prey",self.x+(24*math.cos(self.theta)), self.y+(24*math.sin(self.theta)), self.theta)
                pops.addPrey(newPrey)
                self.reproduceTimer = 0
                self.reproduceCount = 0
                self.reproduceDelay = random.randint(160,200) - len(Population.Populations.getPopulations().allPrey())/10
                self.state = WANDERING
        self.clearComs()

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
        if (self.canvas != None): self.canvas.delete(self.name)

    def alert(self, dir):
        """
        Recieve an alert from another prey about a predator location
        """
        self.coms.append(dir)

    def clearComs(self):
        self.coms.clear()
