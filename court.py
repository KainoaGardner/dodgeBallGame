from settings import *
import math
import pygame

def displayCourt(screen):
    screen.fill(DARKGRAY)
    pygame.draw.rect(screen,COURTCOLOR,(EDGEGAP,EDGEGAP,WIDTH - EDGEGAP * 2,HEIGHT - EDGEGAP * 2))

def drawCountLines(screen):
    pygame.draw.line(screen,RED,(EDGEGAP,EDGEGAP),(WIDTH - EDGEGAP,EDGEGAP),10)
    pygame.draw.line(screen, RED, (EDGEGAP, HEIGHT - EDGEGAP), (WIDTH - EDGEGAP, HEIGHT - EDGEGAP), 10)
    pygame.draw.line(screen, RED, (EDGEGAP, EDGEGAP), (EDGEGAP, HEIGHT - EDGEGAP), 10)
    pygame.draw.line(screen, RED, (WIDTH - EDGEGAP, EDGEGAP), (WIDTH - EDGEGAP, HEIGHT - EDGEGAP), 10)
    pygame.draw.line(screen,RED,(WIDTH // 2, EDGEGAP),(WIDTH // 2,HEIGHT - EDGEGAP),10)
    pygame.draw.circle(screen,RED,(WIDTH // 2,HEIGHT // 2),WIDTH // 10,10)

def resetRound():
    pass


class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,radius):
        super().__init__()
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.radius = radius
        self.hit = False
        self.friction = 0.2
        self.state = "1"
        self.hitCoolDown = 0

    def collide(self,center,playerHalfSize):
        if (self.x - self.radius < center[0] + playerHalfSize and self.x + self.radius > center[0] - playerHalfSize) and (self.y - self.radius < center[1] + playerHalfSize and self.y + self.radius > center[1] - playerHalfSize):
            return True

        return False

    def update(self):
        self.x += self.xVel
        self.y += self.yVel

        angle = math.atan2(self.yVel,self.xVel)
        xFriction = abs(math.cos(angle) * self.friction)
        yFriction = abs(math.sin(angle) * self.friction)

        if self.xVel > 0:
            self.xVel -= min(xFriction,self.xVel)
        elif self.xVel < 0:
            self.xVel += max(xFriction, self.xVel)

        if self.yVel > 0:
            self.yVel -= min(yFriction,self.yVel)
        elif self.yVel < 0:
            self.yVel += max(yFriction, self.yVel)

        if self.x + self.xVel - self.radius < EDGEGAP or self.x + self.xVel + self.radius > WIDTH - EDGEGAP:
            self.xVel *= -1
        if self.y + self.yVel - self.radius < EDGEGAP or self.y + self.yVel + self.radius > HEIGHT - EDGEGAP:
            self.yVel *= -1

        if abs(self.xVel) < 5 and abs(self.yVel) < 5:
            self.state = "stop"

        if self.hit == True:
            self.hitCoolDown += 1
        if self.hitCoolDown > 3:
            self.hitCoolDown = 0
            self.hit = False

        if self.xVel > 25:
            self.xVel = 25
        if self.xVel < -25:
            self.xVel = -25

        if self.yVel > 25:
            self.yVel = 25
        if self.yVel < -25:
            self.yVel = -25

        if self.x < EDGEGAP:
            self.x = EDGEGAP
        if self.x > WIDTH - EDGEGAP:
            self.x = WIDTH - EDGEGAP
        if self.y < EDGEGAP:
            self.y = EDGEGAP
        if self.y > HEIGHT - EDGEGAP:
            self.y = HEIGHT - EDGEGAP

    def display(self,screen):
        self.update()
        if self.state == "stop":
            pygame.draw.circle(screen,WHITE,(self.x,self.y),self.radius)
        elif self.state == "0":
            pygame.draw.circle(screen,YELLOW,(self.x,self.y),self.radius)
        elif self.state == "1":
            pygame.draw.circle(screen,BLUE,(self.x,self.y),self.radius)

        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius + 1,5)


ballGroup = pygame.sprite.Group()
ballGroup.add(Ball(WIDTH//2,HEIGHT // 2,30))
ballGroup.add(Ball(WIDTH//2,HEIGHT * 1/3,30))
ballGroup.add(Ball(WIDTH//2,HEIGHT * 2/3,30))

