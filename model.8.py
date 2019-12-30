# -*- coding: utf-8 -*-
#Created on Wed Nov 27 10:42:28 2019

"""
This model uses Tkinter to create a standard GUI.
When you run the code, two windows should appear
on your screen ('Figure 1' and 'Model').
In the top left of the 'Model' window, please select
'Model' and then 'Run model' from the drop down menu.
"""

# import libraries  
import requests
import bs4
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import agentframework6
import csv
import matplotlib.animation
import tkinter


# Obtain xy data from the web.
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
#print(td_ys)
#print(td_xs)

# define number of iterations and neighbourhood size
num_of_iterations = 10
neighbourhood = 20


# Initialise the GUI - set figure size and axes 
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_autoscale_on(False)


# Read in the in.txt - this initialises the environment
f = open('in.txt', newline='') 
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
environment = [] 
for row in reader:
    rowlist = [] 
    environment.append(rowlist)				
    for value in row:
        rowlist.append(value)				
         				
f.close() 	
        
            
def setup():
    """
    This function initialises the agents and predators. The number of agents (sheep)
    and the number of predators are defined by the GUI sliders.
    """
    global num_of_agents # Global variable defining number of sheep
    num_of_agents = scale_agents.get() # Number of sheep obtained from GUI slider
    global num_of_predators # Global variable defining number of predators
    num_of_predators = scale_predators.get() # Number of predators obtained from GUI slider 
    
    global agents 
    agents = [] # Create agents list - populated by agentframework
    global predators
    predators = [] # Create predators list - populated by agentframework 
    for i in range(num_of_agents):
        y = int(td_ys[i].text)  
        x = int(td_xs[i].text) 
        agents.append(agentframework6.Agent(environment, agents, x, y))
    for i in range(num_of_predators):
        predators.append(agentframework6.predator(environment, agents, x, y))

carry_on = True	

def update(frame_number):
    """
    This function animates the agents and predators, plots the environment and creates
    a colour bar to show the environment density.
    """
    fig.clear() 
    global carry_on 
    
    # Plot the environment 
    matplotlib.pyplot.xlim(0, len(environment)) # Define the x limits for the environment 
    matplotlib.pyplot.ylim(0, len(environment[0])) # Define the y limits for the environment
    matplotlib.pyplot.imshow(environment, vmin=0, vmax=250)
    matplotlib.pyplot.colorbar(shrink = 0.85, label='Environment density') # Initialise colour bar
    
    for i in range(len(agents)): # Animate agents using agentframework
        agents[i].move() 
        agents[i].eat()  
        agents[i].sick() 
        agents[i].share_with_neighbours(neighbourhood) 
    for i in range(len(predators)): # Animate agents using agentframework
        predators[i].move() 
        
        
        if random.random() < 0.000001: # Agents carry on depending on num of iterations  
            carry_on = False
    
    
    for i in range(len(agents)):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y, c = "white") # Sheep are white circles in the animation
    for i in range(len(predators)):
        matplotlib.pyplot.scatter(predators[i].x,predators[i].y, marker = "x", c = "red") # Predators are red crosses in the animation 
        #print(agents[i][0],agents[i][1])
    
def gen_function():
    """
    This function acts as a stopping condition for the animation.
    """
    a = 0
    global carry_on 
    while (a < 99999) & (carry_on): # Agents carry on depeding on num of iterations
        yield a			
        a = a + 1


def run():
    """
    This function runs the model in the form of an animation.
    """
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()

def close():
    """
    This function closes the model.
    """
    root.destroy()
    
# Sets up the GUI
root = tkinter.Tk()
root.wm_title("Model")
menubar = tkinter.Menu(root)
root.config(menu=menubar)
model_menu = tkinter.Menu(menubar)
menubar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run, state="normal")
model_menu.add_command(label="Close model", command=close)

canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

# Adds GUI sliders and buttons

# Defines the slider for the number of agents (sheeps)
scale_agents = tkinter.Scale(root, bd=5, from_=0, label= "1. Choose the number of sheep:", 
                      length=200, orient='horizontal', resolution=1, to=100)
scale_agents.pack(padx=5, pady=5)

# Defines the slider for the number of predators
scale_predators= tkinter.Scale(root, bd=5, from_=0, label= "2. Choose the number of predators:",
                      length=200, orient='horizontal', resolution=1, to=5)
scale_predators.pack(padx=5, pady=5)

# Defines the "set up" button 
butt1 = tkinter.Button(root, command = setup, text = "3. Press here to set up the field")
butt1.pack(padx=5, pady=5)

# Defines the "run" button to start the model
butt2=tkinter.Button(root, command=run, text="Start the ABM")
butt2.pack(padx=5, pady=5)

# Defines the "quit" button to stope the model
butt3=tkinter.Button(root, command=close, text="Quit")
butt3.pack(padx=5, pady=5)

tkinter.mainloop()