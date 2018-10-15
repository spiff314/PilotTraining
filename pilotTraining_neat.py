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

def potential(obsList,x,y):
    
    potVal = 0
    
    # Calculating the potential around each obs
    for i in obsList:
        xPos, yPos = i        
        potVal += gauss(xPos,yPos,x,y,60,255)
    
    # Calculating the potential from the borders of the game
    
    mapSize = 750
    
    wall = np.array(range(0,mapSize))
    
    potVal += np.sum(gauss(0,wall,x,y,15,255))    
    potVal += np.sum(gauss(mapSize,wall,x,y,15,255))
    potVal += np.sum(gauss(wall,0,x,y,15,255))
    potVal += np.sum(gauss(wall,mapSize,x,y,15,255))
    
    return -potVal
    
       

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        
        playerPotential = 0
        #net = neat.nn.FeedForwardNetwork.create(genome, config)
        net = neat.nn.RecurrentNetwork.create(genome,config)
        Game = ptt.game()
        alive = True
        direction = ""
        
        while alive:
            background, score, alive, posList, playerPos = Game.evovle_game(direction)
            
            """
            #Showin the potential landscape
            potentialLandscape = np.zeros((500,500), np.float64)
            # Painting the potential
            for x in range(0,500):
                for y in range(0,500):
                    pot = potential(posList,x,y)
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
            
            """
            newDim = 50
            padDim = 120
            grayPadding = np.zeros((padDim,padDim), np.uint8)
            grayBackground = cv2.cvtColor(background,cv2.COLOR_BGR2GRAY)
            grayBackground = cv2.resize(grayBackground,(newDim,newDim))
            
            invDirectionX = (playerPos[0]/750.0)
            invDirectionY = (playerPos[1]/750.0)
            offsetY = int(padDim/2-int(newDim*invDirectionY))
            offsetX = int(padDim/2-int(newDim*invDirectionX))
            
            
            grayPadding[offsetY:offsetY+grayBackground.shape[0],offsetX:offsetX+grayBackground.shape[1]] = grayBackground
            grayBackground = grayPadding[int(padDim/2-newDim/2):int(padDim/2+newDim/2),int(padDim/2-newDim/2):int(padDim/2+newDim/2)]
            """
            
            #cv2.imshow("Padding",grayPadding)
            #cv2.imshow("grayBackground", grayBackground)
            cv2.imshow("Game", background)
            cv2.waitKey(10)
            velocity = 2*20
            
            inputs = [(potential(posList,playerPos[0]-velocity,playerPos[1]-velocity)),
                      (potential(posList,playerPos[0]-2*velocity,playerPos[1]-2*velocity)),
                      (potential(posList,playerPos[0]-velocity,playerPos[1])),
                      (potential(posList,playerPos[0]-2*velocity,playerPos[1])),
                      (potential(posList,playerPos[0]-velocity,playerPos[1]+velocity)),
                      (potential(posList,playerPos[0]-2*velocity,playerPos[1]+2*velocity)),
                      (potential(posList,playerPos[0],playerPos[1]-velocity)),
                      (potential(posList,playerPos[0],playerPos[1]-2*velocity)),
                      (potential(posList,playerPos[0],playerPos[1]+velocity)),
                      (potential(posList,playerPos[0],playerPos[1]+2*velocity)),
                      (potential(posList,playerPos[0]+velocity,playerPos[1]-velocity)),
                      (potential(posList,playerPos[0]+2*velocity,playerPos[1]-2*velocity)),
                      (potential(posList,playerPos[0]+velocity,playerPos[1])),
                      (potential(posList,playerPos[0]+2*velocity,playerPos[1])),
                      (potential(posList,playerPos[0]+velocity,playerPos[1]+velocity)),
                      (potential(posList,playerPos[0]+2*velocity,playerPos[1]+2*velocity))]
            
            #print("Size = ", grayBackground.reshape((2500,1)).shape)
            #inputs = grayBackground.reshape((grayBackground.shape[0]*grayBackground.shape[1],1))
            playerPotential += potential(posList,playerPos[0],playerPos[1])+300
            
            
            #output = net.activate(np.array(posList).flatten())
            output = net.activate(inputs)
            
            action = np.argmax(output)
            if action == 0 and output[action] > 0.95:
                direction = "w"
            elif action == 1 and output[action] > 0.95:
                direction = "s"
            elif action == 2 and output[action] > 0.95:
                direction = "a"
            elif action == 3 and output[action] > 0.95:
                direction = "d"
            
            
            #Kill it if it reaches 100k
            if score >= 100000:
                print("Survived more than 100.000 frames!")
                alive = False
            
        #print(score)
        print(score)
        #genome.fitness = playerPotential 
        genome.fitness = float(score)
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
    # Run for up to 300 generations.
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
