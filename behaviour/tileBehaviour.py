"""
* Title : tileBehaviour.py
* Desc : TileBehaviour class and some basics behaviours
* Create Date : 17/11/18
* Last Mod : 19/11/18
* TODO:
    - Add more functions
    - More dedicated elements here
"""

import pygame



class TileBehaviour(object):
    def init(self, isoTile):
        pass

    def update(self, isoTile, deltaTime):
        pass


class TileBlinkBehaviour(TileBehaviour):
    def __init__(self, frq, duration, color):
        self._frq = frq
        self._color = color
        self._duration = duration
        self._currentTime = 0
        self._blinking = False
        self._blinkSurface = None
        self._originSurface = None

    def init(self, isoTile):
        tileImg = isoTile.getImage()
        self._blinkSurface = tileImg.copy().convert_alpha()
        self._originSurface = tileImg.copy()
        for x in range(0, self._blinkSurface.get_width()):
            for y in range(0, self._blinkSurface.get_height()):
                if self._blinkSurface.get_at((x, y)).a != 0:
                    self._blinkSurface.set_at((x, y), self._color)
        self._originSurface.blit(self._blinkSurface, (0, 0))
        self._blinkSurface = self._originSurface.copy()
        self._originSurface = tileImg.copy()

    def update(self, isoTile, deltaTime):
        self._currentTime += deltaTime / 1000
        if self._blinking and self._currentTime >= self._duration:
            isoTile.setImage(self._originSurface)
            self._blinking = False
            self._currentTime = 0
        elif not self._blinking and self._currentTime >= self._frq:
            isoTile.setImage(self._blinkSurface)
            self._blinking = True
            self._currentTime = 0
