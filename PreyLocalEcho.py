# Model for the prey that have local communication which echos through prey
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
            
            """
            This is our sending out of the communication. Doesn't use a full triple since this doesn't repeat through 
            the prey, it just occurs once and any near enough hear.

            For the echoing communication, the com also includes a list of all those that have read it, so it doesn't infinitely
            chain between prey. Instead each prey will only recieve each alert at most once

            Since this is just the spawning of the alert, we only need to add our current prey name to it. 
            The actual echoing occurs in alert(self) since it is depth first. Breadth first doesn't work since we would have to do it 
            here and then there would be issues with passing alerts on that might not exist anymore. 
            Depth first ensures that they are only communicated in the single pass they exist. Breadth first *could* (although its
            unlikely) send the alert through to new prey even after it has been resolved or doesn't exist anymore which is an issue
            """
            for otherPrey in pops.allPrey():
                if otherPrey == self:
                    continue
                if (self.distanceTo(otherPrey) < PERCEPTION_DISTANCE):
                    targetTheta = math.atan2(otherPrey.y - self.y, otherPrey.x - self.x)
                    if (abs(targetTheta) > (3.0*math.pi)/2): 
                        otherPrey.alert([EAST, 0, [self]]) # For the direction, we use the opposite since it is to be intepreted by the reciever
                    elif(targetTheta > math.pi/2):
                        otherPrey.alert([0,NORTH, [self]])
                    elif(targetTheta < -math.pi/2):
                        otherPrey.alert([0,SOUTH, [self]])
                    else:
                        otherPrey.alert([WEST, 0, [self]])

        if (self.state == WANDERING):
            for pred in pops.allPred():
                if (self.distanceTo(pred) < PERCEPTION_DISTANCE): 
                    self.state = FLEEING         
            if (self.state == WANDERING):
                if (len(self.coms) > 0):
                    """
                    Find the alert that is the closest using proximity.
                    Then move away from this one. Since they can all be varying distance, we only want to move away from the closest
                    since we can assume that predator is the biggest threat
                    """
                    chosenDir = []
                    chosenDist = 2000
                    for com in self.coms:
                        if com[0] + com[1] < chosenDist:
                            chosenDir = com
                    oppositeTheta = math.atan2(chosenDir[1], chosenDir[0])
                    """
                    # THESE PRINTS SHOW THE CHAINS OF DIRECTION AND THE RESULT OF THE ECHOING COMMUNICATION
                    print("GOING THROUGH: ")
                    for name in chosenDir[2]:
                        print(" | " + str(name.name))
                    print("With direction: " + str(math.degrees(oppositeTheta)))
                    """
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
                newPrey = Prey(self.canvas, "prey")
                newPrey.setLocation(self.x+(8*math.cos(self.theta)), self.y+(8*math.sin(self.theta)))
                newPrey.theta = self.theta
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
        Recieve an alert from another prey about a predator. 
        This will chain to other prey in range if possible

        This also needs to carry on the chain of direction from the original predator.

        Each alert is depth first through the prey, so when we have lots of echos the approzimations become more extreme since it only uses 
        North East South West as directions. 
        """
        self.coms.append(dir)
        alreadyAlerted = dir[2]
        for otherPrey in Population.Populations.getPopulations().allPrey():
            if otherPrey in alreadyAlerted or otherPrey == self:
                continue
            if (self.distanceTo(otherPrey) < PERCEPTION_DISTANCE):
                targetTheta = math.atan2(otherPrey.y - self.y, otherPrey.x - self.x)
                if (abs(targetTheta) > (3.0*math.pi)/2): 
                    otherPrey.alert([dir[0] + EAST, dir[1], dir[2] + [self]]) # For the direction, we use the opposite since it is to be intepreted by the reciever
                elif(targetTheta > math.pi/2):
                    otherPrey.alert([dir[0], dir[1] + NORTH, dir[2] + [self]])
                elif(targetTheta < -math.pi/2):
                    otherPrey.alert([dir[0],dir[1] + SOUTH, dir[2] + [self]])
                else:
                    otherPrey.alert([dir[0] + WEST, dir[1], dir[2] + [self]])


    def clearComs(self):
        self.coms.clear()
