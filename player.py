import pygame
import math
import random
from settings import *
from court import ballGroup,Ball


pygame.font.init()
pygame.init()

throwSound = pygame.mixer.Sound("audio/throw.wav")
throwSound.set_volume(.2)
playerHit = pygame.mixer.Sound("audio/playerhit.wav")
playerHit.set_volume(.3)

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

        self.pressed = False

        self.mos = pygame.mouse.get_pos()
        self.angle = 0
        self.getAngle()
        self.point = ()
        self.armLength = self.width
        self.getPoint()

        self.hitCount = 0
        self.playerHit = False
        self.immuneCooldown = 0

        self.scoreFont = pygame.font.Font("font/LEMONMILK-Regular.otf",WIDTH // 2)
        self.scoreText = self.scoreFont.render(str(self.hitCount),True,COURTCOLORLIGHT)
        self.holdBall = None

        self.addBallCount = 0

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

        if keys[pygame.K_SPACE] and self.holdBall != None and self.pressed == False:
            self.shootBall()
            throwSound.play()
            self.pressed = True

        if keys[pygame.K_SPACE] == False:
            self.pressed = False


        if keys[pygame.K_r]:
            for ball in ballGroup:
                ball.hit = False


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
            if ball.collide(self.point,self.width // 2):
                if ball.state == "stop" and self.holdBall == None:
                    self.holdBall = ball

            if ball.collide(self.center, self.width // 3):
                if ball.state != str(self.turn) and ball.state != "stop" and self.playerHit == False:
                    self.playerHit = True
                    self.hitCount += 1
                    playerHit.play()
                    self.scoreText = self.scoreFont.render(str(self.hitCount), True, COURTCOLORLIGHT)

    def immune(self):
        if self.immuneCooldown > FPS * 2:
            self.playerHit = False
            self.immuneCooldown = 0
        if self.playerHit == True:
            self.immuneCooldown += 1

    def addBall(self):
        if self.addBallCount > FPS * 30 and self.turn == 1:
            self.addBallCount = 0
            ballGroup.add(Ball(WIDTH // 2,random.randint(EDGEGAP,HEIGHT - EDGEGAP),30))
        if len(ballGroup) < 9:
            self.addBallCount += 1

    def grabBall(self):
        if self.holdBall != None:
            self.holdBall.x = self.point[0]
            self.holdBall.y = self.point[1]
            self.holdBall.xVel = 0
            self.holdBall.yVel = 0

    def shootBall(self):
        xVel = math.cos(math.radians(self.angle)) * 25
        yVel = math.sin(math.radians(self.angle)) * 25
        self.holdBall.xVel += xVel
        self.holdBall.yVel += yVel
        self.holdBall.state = str(self.turn)
        self.holdBall = None

    def update(self,screen):
        self.addBall()
        self.getPoint()
        self.immune()
        self.mos = pygame.mouse.get_pos()
        self.move()
        self.getBallCollision()
        self.grabBall()
        self.display(screen)

    def displayScore(self,screen):
        if self.turn == 1:
            screen.blit(self.scoreText,((WIDTH // 2 - EDGEGAP) // 2 - self.scoreText.get_width() // 2 + EDGEGAP,HEIGHT // 2 - self.scoreText.get_height() // 2))
        else:
            screen.blit(self.scoreText,((WIDTH - EDGEGAP - WIDTH // 2) // 2 - self.scoreText.get_width() // 2 + WIDTH // 2,HEIGHT // 2 - self.scoreText.get_height() // 2))

    def display(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height),5)
        if self.playerHit:
            pygame.draw.circle(screen,WHITE,self.center,self.width,5)
        pygame.draw.line(screen, BLACK, (self.center[0], self.center[1]), (self.point[0], self.point[1]), 10)
