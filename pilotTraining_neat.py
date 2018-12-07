# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 14:38:11 2018

@author: ft8510
"""

from __future__ import print_function
import os
import neat
import visualize
import pilotTraining_terminal as ptt
import cv2
import numpy as np
import matplotlib.pyplot as plt

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
 
mapSize = 750

"""
Game = ptt.game()
#for i in range(0,3):
background, score, alive, posList = Game.evovle_game("w")

posList = np.array(posList)
print(posList)
print(posList.flatten())

cv2.imshow("background",background)
cv2.waitKey(0)
    

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

"""


def gauss(centerX,centerY,x,y,width,amplitude):
    
    return amplitude * np.exp( - ( (x-centerX)**2/(2*width**2) + (y-centerY)**2/(2*width**2)  ) )
    
    
def potential(obsList,x,y,velocityList):
    
    potVal = 0
    mapSize = 750
    
    for i in  range(0,len(obsList)):
    #for i in obsList:
        xPos, yPos = obsList[i]
        xVel, yVel = velocityList[i]
        amplitude = 255
        width = 255
        
        
        #xVel, 
        #Calculating the potential around each obs
        #potVal += gauss(xPos,yPos,x,y,60,255)
        
        # Angle between the velocity vector of the obstacle and 'retningsvektor' to the player
        r = np.array([x-xPos,y-yPos])
        v = np.array([xVel,yVel])
        dot = np.dot(r,v)
        
        angle = np.arccos( dot / (np.linalg.norm(r)*np.linalg.norm(v)))
        
        if np.abs(angle) < np.pi/4:
            # Only interested in the maximum potential value
            potVal = max(potVal,gauss(xPos,yPos,x,y,width,amplitude))
        
    
    
    # Check if the max potential value rises from one of the borders
    #potVal = max(potVal,gauss(0,y,x,y,60,255))
    #potVal = max(potVal,gauss(0,mapSize-y,x,y,60,255))
    #potVal = max(potVal,gauss(x,0,x,y,60,255))
    #potVal = max(potVal,gauss(mapSize-x,0,x,y,60,255))
    
    """
    # Calculating the potential from the borders of the game
    wall = np.array(range(0,mapSize))
    potVal += np.sum(gauss(0,wall,x,y,15,255))    
    potVal += np.sum(gauss(mapSize,wall,x,y,15,255))
    potVal += np.sum(gauss(wall,0,x,y,15,255))
    potVal += np.sum(gauss(wall,mapSize,x,y,15,255))
    """
    
    return potVal
    
       

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        
        
        #net = neat.nn.FeedForwardNetwork.create(genome, config)
        net = neat.nn.RecurrentNetwork.create(genome,config)
        Game = ptt.game()
        alive = True
        direction = ""
        potentialScore = 0
        
        while alive:
            background, score, alive, posList, playerPos, velList = Game.evovle_game(direction)
                                 
            velocity = 2*20             # X                             Y
            positionsForPotential = [[playerPos[0]-2*velocity,  playerPos[1]-2*velocity],
                                     [playerPos[0]-2*velocity,  playerPos[1]-velocity],
                                     [playerPos[0]-2*velocity,  playerPos[1]],
                                     [playerPos[0]-2*velocity,  playerPos[1]+velocity],
                                     [playerPos[0]-2*velocity,  playerPos[1]+2*velocity],
                                     [playerPos[0]-velocity,    playerPos[1]-2*velocity],
                                     [playerPos[0]-velocity,    playerPos[1]-velocity],
                                     [playerPos[0]-velocity,    playerPos[1]],
                                     [playerPos[0]-velocity,    playerPos[1]+velocity],
                                     [playerPos[0]-velocity,    playerPos[1]+2*velocity],
                                     [playerPos[0],             playerPos[1]-2*velocity],
                                     [playerPos[0],             playerPos[1]-velocity],
                                     [playerPos[0],             playerPos[1]+velocity],
                                     [playerPos[0],             playerPos[1]+2*velocity],
                                     [playerPos[0]+velocity,    playerPos[1]-2*velocity],
                                     [playerPos[0]+velocity,    playerPos[1]-velocity],
                                     [playerPos[0]+velocity,    playerPos[1]],
                                     [playerPos[0]+velocity,    playerPos[1]+velocity],
                                     [playerPos[0]+velocity,    playerPos[1]+2*velocity],
                                     [playerPos[0]+2*velocity,  playerPos[1]-2*velocity],
                                     [playerPos[0]+2*velocity,  playerPos[1]-1*velocity],
                                     [playerPos[0]+2*velocity,  playerPos[1]],
                                     [playerPos[0]+2*velocity,  playerPos[1]+velocity],
                                     [playerPos[0]+2*velocity,  playerPos[1]+2*velocity]]
            
            
            inputs = []
            for i in positionsForPotential:
                if i[0] < mapSize and i[0] >= 0 and i[1] < mapSize and i[1] >= 0:
                    #cv2.circle(background,(i[0],i[1]),5,(0,0,255),-1)
                    pot = potential(posList,i[0],i[1],velList)
                    inputs.append(pot)
                    #print(pot)
                else:
                    inputs.append(255)
                               
            """     
            #Showing the potential landscape
            potentialLandscape = np.zeros((mapSize,mapSize), np.float64)
            # Painting the potential
            for x in range(0,mapSize):
                for y in range(0,mapSize):
                    pot = potential(posList,x,y,velList)
                    #print(pot)
                    potentialLandscape[y,x] =pot# np.array([pot,pot,pot])
            
            cv2.imshow("potentialLandscape",potentialLandscape)
            cv2.imshow("Game", background)
            plt.figure()
            #plt.imshow(np.sqrt(np.sqrt(potentialLandscape/np.max(potentialLandscape))),cmap = "hot")
            plt.imshow(potentialLandscape,vmin=0,vmax=np.max(potentialLandscape))
            plt.colorbar()        
            cv2.waitKey(0) 
            """

                       
            #cv2.imshow("Game", background)
            #cv2.waitKey(10)
            
            #output = net.activate(np.array(posList).flatten())
            output = net.activate(inputs)
            
            potentialAtOldLocation = potential(posList,playerPos[0],playerPos[1],velList)
            potentialAtNewLocation = potentialAtOldLocation
            
            action = np.argmax(output)
            if action == 0 and output[action] > 0.95:
                direction = "w"
                potentialAtNewLocation = potential(posList,playerPos[0],playerPos[1]-velocity,velList)
            elif action == 1 and output[action] > 0.95:
                direction = "s"
                potentialAtNewLocation = potential(posList,playerPos[0],playerPos[1]+velocity,velList)
            elif action == 2 and output[action] > 0.95:
                direction = "a"
                potentialAtNewLocation = potential(posList,playerPos[0]-velocity,playerPos[1],velList)
            elif action == 3 and output[action] > 0.95:
                direction = "d"
                potentialAtNewLocation = potential(posList,playerPos[0]+velocity,playerPos[1],velList)
            
            
            #Kill it if it reaches 100k
            if score >= 100000:
                print("Survived more than 100.000 frames!")
                alive = False
        
            diffInPotentialAtLocations = potentialAtNewLocation - potentialAtOldLocation
            if diffInPotentialAtLocations <= 0: potentialScore -= diffInPotentialAtLocations/255.0
        
        #print(score,potentialScore)
        
        #genome.fitness = float(score + potentialScore)
        #print(potentialScore)
        genome.fitness = float(potentialScore)
        del(Game) 
            
            
def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))
    
    # Run for up to 1500 generations.
    winner = p.run(eval_genomes, 1500)
    
    # Display the winning genome.
    
    print('\nBest genome:\n{!s}'.format(winner))
    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.RecurrentNetwork.create(winner, config)
    
    """
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))
    """
    node_names = {-1:'O1', -2: 'O2', -3: 'O3', 0:'O4'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
    
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    #p.run(eval_genomes, 10)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
