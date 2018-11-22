"""
* Title : isoGrid.py
* Desc : IsoGrid class
* Create Date : 15/11/18
* Last Mod : 21/11/18
* TODO:
    - Check cellSize in some ways ?
    - Use tile size
    - Implement direction / sorting
    - Consider tile mvt without grid mvt ?
    - Static grid option : Render grid once
    - Take in consideration grid anchoring
"""

import logging
import pygame
import copy


class IsoGrid(object):

    def __init__(self, cellSize, size=(-1, -1, -1), anchor=(0, 0), debug=False):
        """
        Init the grid
        :param cellSize: (width, depth, height)
        :param size: (-1, -1, -1) means infinite
        :param anchor (0,0) grid position in cartesian dimension
        """
        self._logger = logging.getLogger(__name__)
        self._cellSize = cellSize
        self._size = size
        self._anchor = anchor

        # k,j,i (height, left, right)
        self._tilesList = None
        self._debug = debug


    def addIsoTiles(self, isoTiles, positions=None):
        if positions is not None and len(isoTiles) != len(positions):
            self._logger.error('Tile list\'s size is different from positions\'s one')
            return
        for idx, tile in enumerate(isoTiles):
            self.addIsoTile(tile, positions[idx] if positions is not None else None)

    def addIsoTile(self, isoTile, position=None):
        isoTileCpy = copy.deepcopy(isoTile)
        position = position if position is not None else isoTile.getPosition()
        isoTileCpy.setPosition(position)
        self._logger.debug('Adding tile {} at {}'.format(isoTile, position))
        i, j, k = position
        w, d, h = isoTileCpy.getSize()

        if self._tilesList is None:
            self._tilesList = {}
        if k not in self._tilesList.keys():
            self._tilesList[k] = {}
        if j not in self._tilesList[k].keys():
            self._tilesList[k][j] = {}
        if i in self._tilesList[k][j].keys() and self._tilesList[k][j][i] is not None:
            self._logger.warning('Tile {} was already occupied : erasing with new one.')
        self._tilesList[k][j][i] = isoTileCpy

    def setDebug(self, debug):
        self._debug = debug

    def getTileAt(self, i, j, k):
        return self._tilesList[k][j][i]

    def changeSorting(self, sorting):
        pass

    def cartesianToIso(self, cartesian, k):
        x, y = cartesian
        i = ((-k * self._cellSize[2] + y) / self._cellSize[1]) + (x / self._cellSize[0])
        j = ((-k * self._cellSize[2] + y) / self._cellSize[1]) - (x / self._cellSize[0])
        return int(-i), int(-j)

    def isoToCartesian(self, iso):
        ti = self._cellSize[0] / 2
        tj = self._cellSize[1] / 2
        tk = self._cellSize[2]
        i, j, k = iso
        nx = i * ti - j * ti
        ny = k * tk + i * tj + j * tj
        return nx, ny

    def isoToCartesianCenter(self, iso):
        ti = self._cellSize[0] / 2
        tj = self._cellSize[1] / 2
        tk = self._cellSize[2]
        i = -iso[0]
        j = -iso[1]
        k = -iso[2]
        nx = i * ti - j * ti
        ny = k * tk + i * tj + j * tj
        return nx + (self._cellSize[0] / 2), ny + (self._cellSize[1] / 2)

    def update(self, deltaTime):
        for k in self._tilesList.keys():
            for j in self._tilesList[k].keys():
                for i in self._tilesList[k][j].keys():
                    self._tilesList[k][j][i].update(deltaTime)

    def displayDebug(self, surface, anchor):
        # Base anchor with custom anchor and removing pivot point of isoTile (center)
        nAnchor = (self._anchor[0] + anchor[0] - (self._cellSize[0] / 2),
                   self._anchor[1] + anchor[1] - (self._cellSize[1] / 2))
        x, y = nAnchor
        pivotBase = (x + (self._cellSize[0] / 2), y + (self._cellSize[1] / 2))
        # Draw axes
        nx, ny = self.isoToCartesianCenter((10, 0, 0))
        pygame.draw.line(surface, (0, 255, 0), pivotBase, (nx + x, ny + y), 2)
        nx, ny = self.isoToCartesianCenter((0, 10, 0))
        pygame.draw.line(surface, (255, 0, 0), pivotBase, (nx + x, ny + y), 2)
        nx, ny = self.isoToCartesianCenter((0, 0, 10))
        pygame.draw.line(surface, (0, 0, 255), pivotBase, (nx + x, ny + y), 2)
        # Draw Grid
        offsetX = 0
        offsetY = (self._cellSize[1] / 2)
        for i in range(0, 30):
            startX, startY = self.isoToCartesianCenter((i, 0, 0))
            endX, endY = self.isoToCartesianCenter((i, 30, 0))
            pygame.draw.line(surface, (255, 0, 255), (startX + x + offsetX, startY + y + offsetY),
                             (endX + x + offsetX, endY + y + offsetY), 2)
        for i in range(0, 30):
            startX, startY = self.isoToCartesianCenter((0, i, 0))
            endX, endY = self.isoToCartesianCenter((30, i, 0))
            pygame.draw.line(surface, (255, 0, 255), (startX + x + offsetX, startY + y + offsetY),
                             (endX + x + offsetX, endY + y + offsetY), 2)


    def displayAll(self, surface, anchor=(0, 0)):
        if self._tilesList is None:
            self._logger.error('Grid is empty: Nothing to display.')
            if self._debug:
                self.displayDebug(surface, anchor)
            return
        # Base anchor with custom anchor and removing pivot point of isoTile
        nAnchor = (self._anchor[0] + anchor[0] - (self._cellSize[0] / 2),
                   self._anchor[1] + anchor[1] - (self._cellSize[1] / 2))
        x, y = nAnchor
        # default direction is down -> top and back -> front and right -> left
        # down -> top
        kDimKeys = list(self._tilesList.keys())
        kDimKeys.sort()
        for k in kDimKeys:
            jDimKeys = list(self._tilesList[k].keys())
            jDimKeys.sort(reverse=True)
            for j in jDimKeys:
                iDimKeys = list(self._tilesList[k][j].keys())
                iDimKeys.sort(reverse=True)
                for i in iDimKeys:
                    nx, ny = self.isoToCartesian((i, j, k))
                    surface.blit(self._tilesList[k][j][i].getImage(), (nx + x, -ny + y))

        if self._debug:
            self.displayDebug(surface, anchor)


    def displayRect(self, surface, size, anchor=(0, 0)):
        if self._tilesList is None:
            self._logger.error('Grid is empty: Nothing to display.')
            if self._debug:
                self.displayDebug(surface, anchor)
            return
        # Base anchor with custom anchor and removing pivot point of isoTile
        nAnchor = (self._anchor[0] + anchor[0] - (self._cellSize[0] / 2),
                   self._anchor[1] + anchor[1] - (self._cellSize[0] / 2))


        if self._debug:
            self.displayDebug(surface, anchor)
