# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 15:12:54 2018

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
import pilotTraining_neat


def eval_genomes(genomes, config):
    
    video =  cv2.VideoWriter('neat_gen103_potential.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (500,500))
    
    for genome_id, genome in genomes:
        
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        Game = ptt.game()
        alive = True
        direction = ""
        
        
        while alive:
            background, score, alive, posList, playerPos = Game.evovle_game(direction)
            
            """
            potentialLandscape = np.zeros((500,500), np.float64)
            # Painting the potential
            for x in range(0,500):
                for y in range(0,500):
                    pot = potential(posList,x,y)
                    #print(x)
                    potentialLandscape[y,x] =pot# np.array([pot,pot,pot])
            
            cv2.imshow("potentialLandscape",potentialLandscape)
            cv2.imshow("Game", background)
            plt.figure()
            plt.imshow(np.sqrt(np.sqrt(potentialLandscape/np.max(potentialLandscape))),cmap = "hot")
            #plt.imshow(potentialLandscape,vmin=0,vmax=np.max(potentialLandscape))
            plt.colorbar()        
            cv2.waitKey(0)
            """
            
            
            #cv2.imshow("Game", background)
            #cv2.waitKey(10)
            video.write(background)
           
            velocity = 20
            inputs = [int(pilotTraining_neat.potential(posList,playerPos[0]-velocity,playerPos[1]-velocity)),
                      int(pilotTraining_neat.potential(posList,playerPos[0]-velocity,playerPos[1])),
                      int(pilotTraining_neat.potential(posList,playerPos[0]-velocity,playerPos[1]+velocity)),
                      int(pilotTraining_neat.potential(posList,playerPos[0],playerPos[1]-velocity)),
                      int(pilotTraining_neat.potential(posList,playerPos[0],playerPos[1]+velocity)),
                      int(pilotTraining_neat.potential(posList,playerPos[0]+velocity,playerPos[1]-velocity)),
                      int(pilotTraining_neat.potential(posList,playerPos[0]+velocity,playerPos[1])),
                      int(pilotTraining_neat.potential(posList,playerPos[0]+velocity,playerPos[1]+velocity))]
            
            
            
            
            output = net.activate(np.array(posList).flatten())
            output = net.activate(inputs)
            
            action = np.argmax(output)
            if action == 0:
                direction = "w"
            elif action == 1:
                direction = "s"
            elif action == 2:
                direction = "a"
            elif action == 3:
                direction = "d"
            else:
                direction = ""
        
        print(score)
        genome.fitness = float(score)
        del(Game) 
    video.release()     

def run(config_file):
    
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    
    # Add a stdout reporter to show progress in the terminal.
    
    #p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    #p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))
    
    
    
    # Run for up to 300 generations.
    #winner = p.run(eval_genomes, 500)
    
    #winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    
    """
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))
    
    
    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
    """
    
    p = neat.Checkpointer.restore_checkpoint('run_potential/neat-checkpoint-103')
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.run(eval_genomes, 1)

    visualize.draw_net(config, p, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)



