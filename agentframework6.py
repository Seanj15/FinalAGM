# -*- coding: utf-8 -*-
#Created on Wed Nov 27 10:56:08 2019


"""
This file contains an agent class. The agents have a location 
(x and y coordinates) in a 2D grid represented by a raster environment.
Each agent will move around in the 2D grid and interact 
with it's environment.
"""

# Imports a random library to generate random numbers
import random

class Agent():
    
    def __init__(self, environment, agents, x, y):
        """
        Initialises the agents
         
        Postional arguments:
        self = simply the instance of the class.
        environment = the raster environment.
        agents = all the sheep in the environment.
        x = the x coordinate for this agent.
        y = the y coordinate for this agent.
        """
        self.environment = environment
        self.agents = agents
        self.store = 0
        self.x = random.randint(0, len(environment))
        self.y = random.randint(0, len(environment[0]))

        
    def move(self):
        """
        Moves the agents in a random direction
        (by changing the x and y coordinates randomly)
        """     
        agentSpeed = 1
        
        if random.random() < 0.5:
            self.x = (self.x + agentSpeed) 
        else:
            self.x = (self.x - agentSpeed)
    
        if random.random() < 0.5:
            self.y = (self.y + agentSpeed) 
        else:
            self.y = (self.y - agentSpeed)
            
        """
        Boundary edge:
         - Stops agents wandering off the edge of the environment.
         - Prevents them from reappearing on the opposite side of the screen.
         """
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > len(self.environment) -1:
            self.x = len(self.environment) -1
        if self.y > len(self.environment) -1:
            self.y = len(self.environment) -1


    def eat(self): 
        """
        The agents eat the environment (by 10 units at a time).
        Numbers realte to the colour of the environment when plotted.
        This results in a gradual change in colour with more iterations.
        """
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        # Get the agents to store what is left.
        elif self.environment[self.y][self.x] > 0: 
            self.store += self.environment[self.y][self.x]
            self.environment[self.y][self.x] = 0
        # If there is no food in it's location, move on.
        else: 
            self.move
            
   
    def sick(self):
        """
        When an agent has a store greater than 100, the 
        agent deposits 50% of their store in their current location.
        """
        if self.store >= 100:
            self.environment[self.y][self.x] =+ 100
            self.store = 50
            
      
    def share_with_neighbours(self, neighbourhood):
        """
        Positional arguements:
        neighbourhood  = Agents distribute their stores 
        equally amongst themselves when in close proximity with each other.
        Proximity is defined by distance.
        """
        for agent in self.agents:
            distance = self.distance_between(agent)
            if distance <= neighbourhood:
                sum = self.store + agent.store
                ave = sum /2
                self.store = ave
                agent.store = ave
            #print("sharing ", str(dist), " " , str(ave))

    def distance_between(self, agent):
        """
        Positional arguements:
        agent = refers to an agent in this class.
        
        Finds the (straight-line) distance between two sets 
        of coordinates (in this case two agents). Agents need 
        to know who is near them and whether or not to interact 
        with other agents.
        """
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5
    
    def __str__(self):
        """
        Returns information about an agents location and store.
        """
        return "Location x = " + str(self._x) + ", y = " + str(self._y) + ", store = " + str(self.store)               
        print(self)   
    

class predator():
    def __init__(self, environment, agents, x, y):
        """
        Initialises the predators
         
        Postional arguments:
        self = simply the instance of the class.
        environment = the raster environment.
        agents = all the sheep in the environment.
        predators = all the predators in the environment 
        x = the x coordinate for this agent.
        y = the y coordinate for this agent.
        """
        self.environment = environment
        self.agents = agents
        self.x = random.randint(0, len(environment))
        self.y = random.randint(0, len(environment))
        self.store = 0
        
        
        
    def move(self):
        """
        Moves the predators in a random direction
        (by changing the x and y coordinates randomly)
        """     
        
        predator_speed = 2 # speed at which predator will move
        
        detection_distance = 20 # distance at which a predator will detect a sheep
        
        nearest_agent = self.find_nearest() # initialises "agent_distance" and "find_nearest" function
        
        distance_of_closest = self.agent_distance(nearest_agent) # variable to define closest sheep.
        
        if distance_of_closest < detection_distance: # if distance of closest sheep is less than the detection distance
            self.move_to_agent(nearest_agent, predator_speed) # predator will move towards closest agent
        else:
            self.move_randomly(predator_speed) # if predator is not within the detection distance, it will move randomly
            
        self.stop_at_fence() # initialises "stop_at_fence" function
            
        eat_distance = 2 # if sheep gets within a distance of 2 the predator will eat the sheep
        
        if distance_of_closest <= eat_distance: 
            self.eat_agent(nearest_agent) # initialises "eat_agent" function
        
       
    

    def agent_distance(self, agent):
        """
        Calculates distance between predator and sheep.
        """
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5
        
    
    def find_nearest(self):
        """
        This function loops through the agent list to find the nearest
        sheep for the predator. 
        """
        closest_agent_distance = 1000
        for agent in self.agents:
            agent_distance = self.agent_distance(agent)
            if agent_distance < closest_agent_distance:
                closest_agent_distance = agent_distance
                closest_agent = agent
        return closest_agent
                
            
    def move_randomly(self, predator_speed):
        """
        This function moves the predator in a random direction.
        """
        if random.random() < 0.5:
            self.x = (self.x + predator_speed) 
        else:
            self.x = (self.x - predator_speed)
    
        if random.random() < 0.5:
            self.y = (self.y + predator_speed) 
        else:
            self.y = (self.y - predator_speed)
        
    def stop_at_fence(self):
        """
        Boundary edge:
         - Stops predators wandering off the edge of the environment.
         - Prevents them from reappearing on the opposite side of the screen.
         """
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > len(self.environment) -1:
            self.x = len(self.environment) -1
        if self.y > len(self.environment) -1:
            self.y = len(self.environment) -1 
    
    def move_to_agent(self, agent, predator_speed):
        """
        This function moves the predator towards the agent. It will move the
        predator either left or right and either up or down depending on the 
        location of the agent.
        """
        if agent.x > self.x:
            self.x = (self.x + predator_speed) 
        else: 
            self.x = (self.x - predator_speed) 
        if agent.y > self.y:
            self.y = (self.y + predator_speed) 
        else: 
            self.y = (self.y - predator_speed)
        
    def eat_agent(self, agent):
        """
        This function removes the agent once the predator has eaten it.
        """
        self.agents.remove(agent)
            
            
    
            
