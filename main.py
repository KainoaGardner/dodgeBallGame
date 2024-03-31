import pygame
from settings import *
from player import Player
from court import displayCourt,ballGroup

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

def main():
    run = True
    player1 = Player(EDGEGAP * 2, HEIGHT // 2 - 50,100,100,YELLOW,0)
    player2 = Player(WIDTH - EDGEGAP * 2 - 100, HEIGHT // 2 - 50, 100, 100, BLUE, 1)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        displayCourt(screen)
        display(screen,player1,player2,ballGroup)


def display(screen,player1,player2,ballGroup):
    player1.update(screen)
    player2.update(screen)
    for ball in ballGroup:
        ball.display(screen)
    pygame.display.update()
    clock.tick(FPS)

main()