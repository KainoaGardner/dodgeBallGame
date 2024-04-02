import pygame
import math
from settings import *
from player import Player
from court import displayCourt,drawCountLines,ballGroup

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

ballHit = pygame.mixer.Sound("audio/ballhit.wav")
ballHit.set_volume(.3)

def main():
    run = True
    player1 = Player(EDGEGAP * 2, HEIGHT // 2 - 50,100,100,YELLOW,0)
    player2 = Player(WIDTH - EDGEGAP * 2 - 100, HEIGHT // 2 - 50, 100, 100, BLUE, 1)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        display(screen,player1,player2)


def display(screen,player1,player2):
    displayCourt(screen)
    player1.displayScore(screen)
    player2.displayScore(screen)
    drawCountLines(screen)
    player1.update(screen)
    player2.update(screen)
    ballCollison(player1,player2)
    for ball in ballGroup:
        ball.display(screen)
    pygame.display.update()
    clock.tick(FPS)

def ballCollison(player1,player2):
    for ball in ballGroup:
        for ball2 in ballGroup:
            if ball != ball2:
                if ball.hit == False and ball2.hit == False:
                    if ball.collide((ball2.x,ball2.y),ball2.radius):
                        xDif = ball2.x - ball.x
                        yDif = ball2.y - ball.y
                        angle = math.atan2(yDif,xDif)
                        ball1Force = math.sqrt(ball.xVel * ball.xVel + ball.yVel * ball.yVel)
                        ball2Force = math.sqrt(ball2.xVel * ball2.xVel + ball2.yVel * ball2.yVel)

                        ball1Forcex = math.cos(angle) * ball1Force * 2/3
                        ball1Forcey = math.sin(angle) * ball1Force * 2/3
                        ball2Forcex = math.cos(angle) * ball2Force * 2/3
                        ball2Forcey = math.sin(angle) * ball2Force * 2/3

                        ball2.xVel += ball1Forcex
                        ball2.yVel += ball1Forcey
                        ball.xVel -= ball1Forcex
                        ball.yVel -= ball1Forcey

                        ball.xVel -= ball2Forcex
                        ball.yVel -= ball2Forcey
                        ball2.xVel += ball2Forcex
                        ball2.yVel += ball2Forcey

                        ball.hit = True
                        ball2.hit = True
                        if not (ball.xVel == 0 and ball.yVel == 0 and ball2.xVel == 0 and ball2.yVel == 0):
                            ballHit.play()


                        if ball != player1.holdBall and ball != player2.holdBall and ball2 != player1.holdBall and ball2 != player2.holdBall:
                            if ball.state != "stop" and ball2.state == "stop":
                                ball2.state = ball.state
                            elif ball2.state != "stop" and ball.state == "stop":
                                ball.state = ball2.state


main()