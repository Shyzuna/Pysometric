"""
* Title : isoTile.py
* Desc : IsoTile class
* Create Date : 15/11/18
* Last Mod : 19/11/18
* TODO:
    - Load default base64 image
    - Resize fct
    - Consider mvt without grid mvt ?
    - Think a way to manage light
    - Use deepcopy on behaviour
"""
import pygame
import logging
import copy


class IsoTile(object):
    def __init__(self, size=(1, 1, 1), image=None, position=None, resize=True, debug=False):
        """
        Init an iso tile
        :param size: in grid unit
        :param image: can be either a path or a pygame.image
        :param position: position on grid
        :param resize: Will resize when added to a grid
        """
        self._logger = logging.getLogger(__name__)
        self._size = size
        if image is not None:
            if isinstance(image, str):
                image = pygame.image.load(image)
        else:
            # Load default image from base64
            pass

        self._image = image.convert_alpha()
        self._position = position
        self._resize = resize
        self._behaviours = {}
        self._debug = debug

    def resize(self, gridSize):
        if self._resize:
           pass

    def setPosition(self, position):
        self._position = position

    def getPosition(self):
        return self._position

    def getSize(self):
        return self._size

    def getImage(self):
        return self._image

    def setImage(self, img):
        self._image = img

    def addBehaviour(self, name, tileBehaviour):
        if name in self._behaviours.keys():
            self._logger.warning('Behaviour already exist : Erasing with new one.')
        behaviourCopy = copy.copy(tileBehaviour)
        self._behaviours[name] = behaviourCopy
        behaviourCopy.init(self)

    def update(self, deltaTime):
        for behaviour in self._behaviours.values():
            behaviour.update(self, deltaTime)

    def __deepcopy__(self, memodict={}):
        newItem = type(self)(
            copy.deepcopy(self._size),
            self._image.copy(),
            copy.deepcopy(self._position),
            copy.deepcopy(self._resize),
            copy.deepcopy(self._debug)
        )
        for name, behaviour in self._behaviours.items():
            newItem.addBehaviour(name, behaviour)
        return newItem