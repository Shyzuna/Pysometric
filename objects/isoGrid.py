"""
* Title : isoGrid.py
* Desc : IsoGrid class
* Create Date : 15/11/18
* Last Mod : 19/11/18
* TODO:
    - Check cellSize in some ways ?
    - Use tile size
    - Implement direction / sorting
    - Consider tile mvt without grid mvt ?
"""

import logging
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

    def update(self, deltaTime):
        for k in self._tilesList.keys():
            for j in self._tilesList[k].keys():
                for i in self._tilesList[k][j].keys():
                    self._tilesList[k][j][i].update(deltaTime)

    def displayAll(self, surface, anchor=None):
        if self._tilesList is None:
            self._logger.error('Grid is empty: Nothing to display.')
            return
        anchor = anchor if anchor is not None else self._anchor
        x, y = anchor
        ti = self._cellSize[0] / 2
        tj = self._cellSize[1] / 2
        tk = self._cellSize[2]
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
                    nx = i * ti - j * ti
                    ny = -k * tk - i * tj - j * tj
                    surface.blit(self._tilesList[k][j][i].getImage(), (nx + x, ny + y))

