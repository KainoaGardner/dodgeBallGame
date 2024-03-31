import pygame
import math
from settings import *
from court import ballGroup


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color,turn):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = (self.x + self.width / 2,self.y + self.height / 2)
        self.color = color
        self.turn = turn
        self.speed = 10
        self.diagSpeed = math.sqrt((self.speed * self.speed) / 2)

        self.mos = pygame.mouse.get_pos()
        self.angle = 0
        self.getAngle()
        self.point = ()
        self.armLength = self.width
        self.getPoint()

        self.holdBall = None

    def move(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_w] and keys[pygame.K_a]) or (keys[pygame.K_w] and keys[pygame.K_d]) or (keys[pygame.K_s] and keys[pygame.K_a]) or (keys[pygame.K_s] and keys[pygame.K_d]):
            speed = self.diagSpeed
        else:
            speed = self.speed
        if keys[pygame.K_w]:
            if self.y - speed > EDGEGAP:
                self.y -= speed
            else:
                self.y = EDGEGAP
        if keys[pygame.K_s]:
            if self.y + speed < HEIGHT - EDGEGAP - self.height:
                self.y += speed
            else:
                self.y = HEIGHT - EDGEGAP - self.height

        if self.turn == 0:
            if keys[pygame.K_a]:
                if self.x - speed > EDGEGAP:
                    self.x -= speed
                else:
                    self.x = EDGEGAP
            if keys[pygame.K_d]:
                if self.x + speed < WIDTH // 2 - self.width:
                    self.x += speed
                else:
                    self.x = WIDTH // 2 - self.width
        else:
            if keys[pygame.K_a]:
                if self.x - speed > WIDTH // 2:
                    self.x -= speed
                else:
                    self.x = WIDTH // 2
            if keys[pygame.K_d]:
                if self.x + speed < WIDTH - EDGEGAP - self.width:
                    self.x += speed
                else:
                    self.x = WIDTH - EDGEGAP - self.width

        if keys[pygame.K_SPACE] and self.holdBall != None:
            self.shootBall()


    def getAngle(self):
        self.center = (self.x + self.width / 2,self.y + self.height / 2)
        xDif = self.mos[0] - self.center[0]
        yDif = self.mos[1] - self.center[1]
        angle = math.atan2(yDif,xDif)
        self.angle = math.degrees(angle)

    def getPoint(self):
        self.getAngle()
        xPoint = self.center[0] + math.cos(math.radians(self.angle)) * self.width
        yPoint = self.center[1] + math.sin(math.radians(self.angle)) * self.width
        self.point = (xPoint,yPoint)

    def getBallCollision(self):
        for ball in ballGroup:
            if ball.collide(self.center,self.width // 2):
                if ball.state == "stop" and self.holdBall == None:
                    self.holdBall = ball
                elif ball.state != str(self.turn):
                    print("die")

    def grabBall(self):
        if self.holdBall != None:
            self.holdBall.x = self.point[0]
            self.holdBall.y = self.point[1]

    def shootBall(self):
        xVel = math.cos(math.radians(self.angle)) * 25
        yVel = math.sin(math.radians(self.angle)) * 25
        self.holdBall.xVel = xVel
        self.holdBall.yVel = yVel
        self.holdBall.state = str(self.turn)
        self.holdBall = None

    def update(self,screen):
        self.getPoint()
        self.mos = pygame.mouse.get_pos()
        self.move()
        self.getBallCollision()
        self.grabBall()
        self.display(screen)

    def display(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))
        pygame.draw.line(screen, WHITE, (self.center[0], self.center[1]), (self.point[0], self.point[1]), 10)