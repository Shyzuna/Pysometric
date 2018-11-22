"""
* Title : main.py
* Desc : Test the Pysometric lib
* Create Date : 15/11/18
* Last Mod : 17/11/18
* TODO:
    - Do key repeat in another way
"""
import pygame

from objects.isoTile import IsoTile
from objects.isoGrid import IsoGrid
from camera.isoCamera import IsoCamera
from behaviour.tileBehaviour import TileBlinkBehaviour
import os

if __name__ == '__main__':

    options = pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF

    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Pysometric')

    isoC = IsoCamera(screen.get_rect(), pygame.Rect(0, 0, 1200, 800), True)
    isoG = IsoGrid((70, 35, 39), debug=True)
    isoC.addGrid('mainGrid', isoG, 0)
    isoC.centerCameraOn('mainGrid', (0, 0, 0))
    tile = IsoTile(image=os.path.join('res', 'images', 'cube.png'))

    clock = pygame.time.Clock()

    for i in range(0, 50):
        for j in range(0, 50):
            isoG.addIsoTile(tile, (i, j, 0))

    isoG.addIsoTile(tile, (5, 5, 1))

    tileBlinkB = TileBlinkBehaviour(0.5, 0.5, pygame.Color(255, 0, 0, 50))
    isoG.getTileAt(5, 5, 1).addBehaviour('blink', tileBlinkB)

    pygame.font.init()
    myFont = pygame.font.Font(os.path.join('res', 'fonts', 'horde.ttf'), 20)

    pygame.key.set_repeat(1, 10)
    stop = False
    while not stop:
        deltaTime = clock.tick(120)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                stop = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    isoC.move((-10, 0))
                if e.key == pygame.K_RIGHT:
                    isoC.move((10, 0))
                if e.key == pygame.K_DOWN:
                    isoC.move((0, 10))
                if e.key == pygame.K_UP:
                    isoC.move((0, -10))
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(isoG.cartesianToIso((x + isoC._originRect.x, y + isoC._originRect.y), 0))

        isoG.update(deltaTime)
        fpsSurface = myFont.render(str(int(clock.get_fps())), 0, (255, 0, 0))

        screen.fill((0, 0, 0))
        isoC.display(screen)
        screen.blit(fpsSurface, (10, 10))
        pygame.display.flip()

    pygame.quit()
