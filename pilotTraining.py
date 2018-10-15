#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 12:54:45 2018

@author: nicolai
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2


green = (0,255,0)
red = (0,0,255)
blue = (255,0,0)
black = (0,0,0)
white = (255,255,255)
cyan = (255,255,0)

width = 500
height = 500

class obstacles(object):
    posX = []
    posY = []
    velX = []
    velY = []
    color = []
    height = 500
    width = 500
    
    rad = []
    circle = []
    
    def __init__(self,canvas,initX,initY,radius,velX,velY,color):
        self.posX = initX
        self.posY = initY
        self.rad = radius
        self.velX = int(velX)
        self.velY = int(velY)
        self.color = color
        self.drawCircle(canvas)
        
        
    def updatePos(self):
               
        if np.abs(self.posX-self.width) <= self.rad:
            self.velX *= -1
        if self.posX <= self.rad:
            self.velX *= -1
        if np.abs(self.posY-self.height) <= self.rad:
            self.velY *= -1
        if self.posY <= self.rad:
            self.velY *= -1
            
        self.setPos(self.posX+self.velX,self.posY+self.velY)
        
    def setPos(self,x,y):
        self.posX = x
        self.posY = y
    
    def getPos(self):
        return (self.posX,self.posY)
    
    def getRad(self):
        return self.rad
        
    def drawCircle(self,canvas):
        cv2.circle(canvas,(self.posX,self.posY),self.rad,black,-1)
        self.updatePos()       
        cv2.circle(canvas,(self.posX,self.posY),self.rad,self.color,-1)
    

class player(object):
    
    def __init__(self,canvas, startPosX,startPosY,color):
        self.posX = startPosX
        self.posY = startPosY
        self.color = color
        self.rad = 15
        cv2.circle(canvas,(self.posX,self.posY),self.rad,self.color,-1)
        
    def getPos(self):
        return(self.posX,self.posY)
    
    def getRad(self):
        return(self.rad)
        
    def drawPlayer(self,canvas):
        cv2.circle(canvas,(self.posX,self.posY),self.rad,cyan,-1)
        
    def moveLeft(self,canvas,velocity):
        cv2.circle(canvas,(self.posX,self.posY),self.rad,black,-1)
        self.posX -= velocity
        cv2.circle(canvas,(self.posX,self.posY),self.rad,cyan,-1)
    
    def moveRight(self,canvas,velocity):
        cv2.circle(canvas,(self.posX,self.posY),self.rad,black,-1)
        self.posX += velocity
        cv2.circle(canvas,(self.posX,self.posY),self.rad,cyan,-1)
    
    def moveUp(self,canvas,velocity):
        cv2.circle(canvas,(self.posX,self.posY),self.rad,black,-1)
        self.posY -= velocity
        cv2.circle(canvas,(self.posX,self.posY),self.rad,cyan,-1)
    
    def moveDown(self,canvas,velocity):
        cv2.circle(canvas,(self.posX,self.posY),self.rad,black,-1)
        self.posY += velocity
        cv2.circle(canvas,(self.posX,self.posY),self.rad,cyan,-1)
    
    def checkForWallCollisions(self):
         if self.posX < self.rad or width - self.posX < self.rad or self.posY < self.rad or height - self.posY < self.rad:
             return True
         else:
             return False
    
def checkForGameOver(obsList,player):
    
    
    for i in obsList:
        
        iX,iY = i.getPos()
        iRad = i.getRad()
        
        pX,pY = player.getPos()
        pRad = player.getRad()
        
        if np.sqrt( (iX-pX)**2+(iY-pY)**2) < iRad+pRad:
            print("Collisions")
            return True
        elif pX < pRad or pRad > width-pX or pY < pRad or pRad > height-pY:
            return True
        
    return False

def game():
    #%% Game Window
    background = np.zeros((height,width,3), np.uint8)
    score = 0   
    #%%  Obstacles   
    obsVelocity = 0.5
    obs1 = obstacles(background,200,150,30,obsVelocity*3,-obsVelocity*7,red)
    obs2 = obstacles(background,450,350,10,obsVelocity*3,obsVelocity*13,blue)
    obs3 = obstacles(background,100,31,24,obsVelocity*7,-obsVelocity*7,green)
    obs4 = obstacles(background,42,42,24,obsVelocity*6,obsVelocity*5,white)   
    obsList = [obs1, obs2, obs3, obs4]
    
    #%% Player
    
    player1 = player(background,int(width/2),400,cyan)
    velocity = 20
    
    #%% Game
    intro = 0
    while(True):
        
        #Draw obstacles and checks for collisions
        if intro > 100:            
            
            for i in obsList:                    
                i.drawCircle(background)
                
            if checkForGameOver(obsList,player1):
                cv2.destroyAllWindows()
                return score, "Game Over"
                        
            player1.drawPlayer(background)
            score += 1
        else:  
            intro += 1
            
        cv2.imshow("the game",background)
        k = cv2.waitKey(10)
        if k == 27:
            break
        elif k == 119: # Move up (w)
            player1.moveUp(background,velocity)
        elif k == 115: # Move down (s)
            player1.moveDown(background,velocity)
        elif k == 97: # Move left (a)
            player1.moveLeft(background,velocity)
        elif k == 100: # Move right (d)
            player1.moveRight(background,velocity)
         
    
    cv2.destroyAllWindows()
    return score, "Player ended the game!"


if __name__ == '__main__':
    print("Let the gamea begin")
    
    status = game()
    
    print(status)












