"""
* Title : isoCamera.py
* Desc : IsoCamera class
* Create Date : 16/11/18
* Last Mod : 23/11/18
* TODO:
"""
import logging
import pygame


class IsoCamera(object):
    def __init__(self, originRect, destinationRect, debug=False):
        self._logger = logging.getLogger(__name__)
        self._originRect = originRect
        self._destinationRect = destinationRect
        self._gridList = {}
        self._gridOrder = {}
        self._cameraSurface = pygame.Surface((originRect[2], originRect[3]))
        self._debug = debug

    def addGrid(self, gridName, isoGrid, gridOrder):
        if gridName in self._gridList.keys():
            self._logger.warning('Grid {} already exists : erasing it with the new one.'.format(gridName))
        self._gridList[gridName] = isoGrid
        if gridOrder in self._gridOrder.values():
            self._logger.warning('A grid is already ordered {} : Grid with same priority will be ordered randomly.')
        self._gridOrder[gridName] = gridOrder

    def debugDisplay(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self._destinationRect, 2)

    def display(self, surface):
        currentOrder = list(self._gridOrder.items())
        currentOrder.sort(key=(lambda item: item[1]))

        self._cameraSurface.fill((0, 0, 0))
        currentAnchor = (-self._originRect.x, -self._originRect.y)
        for gridName, gridOrder in currentOrder:
            self._gridList[gridName].displayRect(self._cameraSurface, currentAnchor)
            #self._gridList[gridName].displayAll(self._cameraSurface, currentAnchor)

        scaledSize = (self._destinationRect.w, self._destinationRect.h)
        scaledSurface = pygame.transform.scale(self._cameraSurface, scaledSize)
        surface.blit(scaledSurface, (self._destinationRect.x, self._destinationRect.y))
        if self._debug:
            self.debugDisplay(surface)

    def displayStatic(self, surface):
        currentOrder = list(self._gridOrder.items())
        currentOrder.sort(key=(lambda item: item[1]))

        self._cameraSurface.fill((0, 0, 0))
        for gridName, gridOrder in currentOrder:
            self._gridList[gridName].displayStatic(self._cameraSurface)

        scaledSize = (self._destinationRect.w, self._destinationRect.h)
        scaledSurface = pygame.transform.scale(self._cameraSurface, scaledSize)
        surface.blit(scaledSurface, (self._destinationRect.x, self._destinationRect.y))
        if self._debug:
            self.debugDisplay(surface)

    def move(self, vector, updateGrids=False):
        self._logger.debug('Moving camera by {}'. format(vector))
        x, y = vector
        self._originRect = self._originRect.move(x, y)
        if updateGrids:
            currentAnchor = (-self._originRect.x, -self._originRect.y)
            for grid in self._gridList.values():
                grid.updateStaticSurface((self._originRect.width, self._originRect.height), currentAnchor)


    def centerCameraOn(self, gridName, isoCoord, updateGrids=False):
        if gridName not in self._gridList.keys():
            self._logger.warning('No Grid named {} : Cannot center on.'.format(gridName))
            return
        centerX, centerY = self._gridList[gridName].isoToCartesianCenter(isoCoord)
        self._originRect.move_ip(centerX - (self._originRect.width / 2), centerY - (self._originRect.height / 2))
        if updateGrids:
            currentAnchor = (-self._originRect.x, -self._originRect.y)
            for grid in self._gridList.values():
                grid.updateStaticSurface((self._originRect.width, self._originRect.height), currentAnchor)
