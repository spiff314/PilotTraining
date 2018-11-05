#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 12:54:45 2018

@author: nicolai
"""

import numpy as np
import cv2


green = (0,255,0)
red = (0,0,255)
blue = (255,0,0)
black = (0,0,0)
white = (255,255,255)
cyan = (255,255,0)

width = 750
height = 750

borderWidth = 15
borderColor = (255,255,255)
fudgeFactor = 0.9

class obstacles(object):
    posX = []
    posY = []
    velX = []
    velY = []
    color = []
    height = 750
    width = 750
    
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
        
        if np.abs(self.posX-self.width) <= fudgeFactor*borderWidth + self.rad :
            self.velX *= -1
        if self.posX <= fudgeFactor*borderWidth + self.rad:
            self.velX *= -1
        if np.abs(self.posY-self.height) <= fudgeFactor*borderWidth + self.rad:
            self.velY *= -1
        if self.posY <= fudgeFactor*borderWidth + self.rad:
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
         if self.posX < fudgeFactor*borderWidth + self.rad or width - self.posX < fudgeFactor*borderWidth + self.rad or self.posY < fudgeFactor*borderWidth + self.rad or height - self.posY < fudgeFactor*borderWidth + self.rad:
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
            return True
        elif pX < pRad or pRad > width-pX or pY < pRad or pRad > height-pY:
            return True
        
    return False



class game(object):
    
    def __init__(self):
        
        # Game Window
        self.background = np.zeros((height,width,3), np.uint8)
        cv2.line(self.background,(0,0),(0,width),borderColor,borderWidth)
        cv2.line(self.background,(height,0),(height,width),borderColor,borderWidth)
        cv2.line(self.background,(0,0),(height,0),borderColor,borderWidth)
        cv2.line(self.background,(0,width),(height,width),borderColor,borderWidth)
        
        self.score = 0
        
        # Obstacles
        self.obsVelocity = 1
        
        self.obs1 = obstacles(self.background,200,150,30,self.obsVelocity*3,-self.obsVelocity*7,white)
        self.obs2 = obstacles(self.background,450,350,24,self.obsVelocity*3,self.obsVelocity*9,white)
        self.obs3 = obstacles(self.background,100,31,24,self.obsVelocity*7,-self.obsVelocity*7,white)
        self.obs4 = obstacles(self.background,42,42,24,self.obsVelocity*6,self.obsVelocity*5,white)   
        
        #velocities = (np.random.rand(4,2)-0.5)*20
        #velocities = [[7 if (np.abs(x) < 3) else x for x in y] for y in velocities]
        #print(velocities)
        #self.obs1 = obstacles(self.background,200,150,30,velocities[0][0],velocities[0][1],red)
        #self.obs2 = obstacles(self.background,450,350,10,velocities[1][0],velocities[1][1],blue)
        #self.obs3 = obstacles(self.background,100,31,24,velocities[2][0],velocities[2][1],green)
        #self.obs4 = obstacles(self.background,42,42,24,velocities[3][0],velocities[3][1],white) 
        
        
        self.obsList = [self.obs1, self.obs2, self.obs3, self.obs4]
        

        # Player
        self.player1 = player(self.background,int(width/2),int(height/2),cyan)
        self.velocity = 20
        self.maxNumberOfCamperFrames = 1000
        self.playerPositionList = []
        self.posList = []
        
    def evovle_game(self,direction): # Direction is a string ("w","s","a","d")
        
        self.posList = []
        alive = True
        
        #Draw obstacles and checks for collisions
        for i in self.obsList:                    
            i.drawCircle(self.background)
            
        if checkForGameOver(self.obsList,self.player1):
            alive = False
            #return self.background, self.score, alive, self.posList
                    
        self.player1.drawPlayer(self.background)
        self.score += 1

        if  direction == "w": # Move up (w)
            self.player1.moveUp(self.background,self.velocity)
        elif direction == "s" : # Move down (s)
            self.player1.moveDown(self.background,self.velocity)
        elif direction == "a": # Move left (a)
            self.player1.moveLeft(self.background,self.velocity)
        elif direction == "d": # Move right (d)
            self.player1.moveRight(self.background,self.velocity)
        else:
            pass
         
        
        #self.posList.append(self.player1.getPos())
        for i in self.obsList:
            self.posList.append(i.getPos())
        
        # Tracking player movement
        self.playerPositionList.insert(0,self.player1.getPos())
        
        if len(self.playerPositionList) > self.maxNumberOfCamperFrames:
            self.playerPositionList.remove(self.playerPositionList[-1])
            
            xstd,ystd = np.std(np.array(self.playerPositionList),axis=0)
            
            if xstd < 0.6*self.velocity and ystd < 0.6*self.velocity:
                print("Camper")
                self.score -= self.maxNumberOfCamperFrames
                alive = False
        
        
        #cv2.destroyAllWindows()
        return self.background, self.score, alive, self.posList, self.player1.getPos()


if __name__ == '__main__':
    print("Let the game begin")
    
    for i in range(0,3):
        
        Game = game()        
        alive = True
        
        while alive:
            
            background, score, alive, posList, playerPos = Game.evovle_game("")
            
            cv2.imshow("game",background)
            
            cv2.waitKey(20)
            
            if not alive:
                print("Game Over")
                cv2.destroyAllWindows()
                del(Game)
    
    
    
    cv2.destroyAllWindows()











