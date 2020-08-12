#This is a simulation of the ideal gas law, PV=nRT. 
#Pressure, volume, moles, and temperature are displayed.
#Each animated particle represents 1 mol of gas. The user can increase or 
#decrease the number of particles by pressing the up and down arrows.
#The user can adjust the piston (increasing or decreasing the volume of the 
#container) using the left and right arrows. 
#With each adjustment, pressure is calculated according to the ideal gas law.
#Temperature remains constant. 
#Collisions of the particles are elastic.

import Draw
import random
import math
import ElasticCollision

particleRadius=10

#draw the canvas
Draw.setCanvasSize(1000,700)
Draw.setBackground(Draw.color(145, 193, 255)) #medium blue

#draw the board
def drawBoard(particles, chamberWidth, \
              temperature, volume, numParticles, pressure, \
              rightWall,maxWidth,topWall,height,leftWall):
    
    Draw.clear()
    
    #draw the chamber
    lightBlue=Draw.color(214, 232, 255)
    Draw.setColor(lightBlue)
    Draw.filledRect(rightWall,topWall,-maxWidth,height)
    
    #draw movable piston
    Draw.setColor(Draw.GRAY)
    #vertical bar with right end at leftWall
    Draw.filledRect(leftWall,topWall,-45,height) 
    #horizontal bar from beginning of canvas to vertical bar
    Draw.filledRect(leftWall,300,-550,75) 
    
    #for each particle, draw it
    red=Draw.color(250, 74, 67)
    Draw.setColor(red)
    for i in range(len(particles)):
        Draw.filledOval(particles[i][0]-particleRadius,\
                        particles[i][1]-particleRadius,\
                        2*particleRadius,2*particleRadius) 
        #center incremented by radius
        #diameter width and height
    
    #draw temp, pressure, mol, vol
    Draw.setColor(Draw.GRAY) #boxes surrounding measurements
    for i in range(170,480,100):
        Draw.filledRect(670,i,280,35) #each box 100 units below prev box
    Draw.setColor(Draw.WHITE)
    Draw.setFontFamily("Courier")
    Draw.setFontSize(24)
    Draw.string("Pressure: %.2f atm" %pressure,675,175)  #rounded to 2 decimals
    Draw.string("Volume: " +str(volume)+ " L",675,275)
    Draw.string("Particles: " +str(numParticles)+ " mol",675,375)
    Draw.string("Temperature: "+str(temperature)+ " K",675,475)
        
    Draw.show()
    
def adjustParticles(particles, leftWall, velocity):
    #for each particle, if it's to the left of the left wall, 
    #move it to the right of the left wall
    for particle in particles:
        #the particle's x cannot be less than radius length away from the wall
        if particle[0]<leftWall+particleRadius:
            particle[0]=leftWall+particleRadius
            #change direction of the particle to be horizontal 
            #(appears pushed by wall, prevents particles from sticking to wall)
            particle[2]=velocity
            particle[3]=0
            
def moveParticles(particles,rightWall,leftWall,topWall,bottomWall):
    
    #increment the particle by its dx and dy
    for particle in particles:
        particle[0]+=particle[2] #add dx to x
        particle[1]+=particle[3] #add dy to y
        
        
    #for each particle, for each of the remaining particles, 
    #if the particles intersected, invoke ElasticCollision
    for i in range (len(particles)):
        for j in range (i+1,len(particles)):
            if particlesIntersect(particles[i],particles[j]):
                ElasticCollision.collide(particles[i],particles[j])    
    
    #if the particle hit a wall, change its direction.
    for particle in particles:
    #don't let it go past left or right side
        #if x is going off side, change x's direction
        if particle[0]<leftWall+particleRadius or \
           particle[0]>rightWall-particleRadius: 
            particle[2]*=-1 #negate dx
        #if y is going off top or bottom, change y's direction
        if particle[1]<topWall+particleRadius or \
           particle[1]>bottomWall-particleRadius: 
            particle[3]*=-1 #negate dy
            
      
def particlesIntersect(a,b): #input: 2 particles
    
    #if the distance between a's center and b's center is less than 
    #the length of the diameter, the particles intersected
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5<2*particleRadius
        

def main():
    #initialize empty list of particles
    particles=[]
    
    #chamber dimensions
    rightWall=650
    maxWidth=600
    topWall=125
    height=425
    bottomWall=topWall+height
    
    #initialize initial width of chamber
    chamberWidth=maxWidth
    leftWall=rightWall-chamberWidth
    
    #speed of particles
    velocity=2
    
    while True: #forever
        #if the user clicked a key, get the new key
        if Draw.hasNextKeyTyped():
            newKey=Draw.nextKeyTyped()
            #if they clicked the left or right arrow, 
            #adjust the chamber width by 50 in that direction 
            #within the bounds of 200-maxWidth
            if newKey=="Left":
                if chamberWidth<maxWidth:
                    chamberWidth+=50
                    leftWall-=50
            elif newKey=="Right":
                if chamberWidth>200:
                    chamberWidth-=50
                    leftWall+=50
                    #adjust particles to stay within new rect
                    adjustParticles(particles, leftWall, velocity) 
            #if they clicked the up arrow, add 10 particles to the list
            #cap particles at 50
            elif len(particles)<50 and newKey=="Up":
                for i in range(10):
                    #set x and y of particle's center
                    #x: between 2 walls of chamber, 
                    #leaving room for particle between center and wall
                    x=random.randint(leftWall+particleRadius,\
                                     rightWall-particleRadius) 
                    #y: between top and bottom of chamber, 
                    #leaving room for particle
                    y=random.randint(topWall+particleRadius,\
                                     bottomWall-particleRadius)
                    
                    #set random dx and dy by choosing a random angle 
                    #and finding the sin and cos of that angle 
                    #(all move distance of 1 based on unit circle, times velocity)
                    angle=random.random()*2*math.pi
                    dx=math.cos(angle)*velocity
                    dy=math.sin(angle)*velocity
                    
                    particles+=[[x,y,dx,dy]]
                    
            #if there are particles in the list and they clicked the down arrow,
            #remove 10 particles from the list
            elif len(particles)>=1 and newKey=="Down": 
                #make a new list, 
                #adding all but the last 10 particles on the particle list
                particles=[particles[i] for i in range(len(particles)-10)]
            
                
        #calculate variables:
        #based on gas law formula PV=nRT 
        temperature=298 #constant (in K)
        volume=chamberWidth #(in L)
        numParticles=len(particles) #each particle represents 1 mol
        R=.08206 #gas constant (in (L*atm)/(mol*k))
        pressure=(numParticles*R*temperature)/volume #(in atm) 
        
           
    
        moveParticles(particles,rightWall,leftWall,topWall,bottomWall)
    
        drawBoard(particles, chamberWidth, temperature, volume, numParticles,\
                  pressure, rightWall,maxWidth,topWall,height,leftWall)
        
main()
                
            