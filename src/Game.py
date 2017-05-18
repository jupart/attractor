from kivy.uix.widget import Widget

import kivent_core
import kivent_cymunk
from kivent_core.systems.position_systems import PositionSystem2D
from kivent_core.systems.rotate_systems import RotateSystem2D
from kivent_core.systems.renderers import RotateRenderer
from kivent_core.systems.gamesystem import GameSystem
from kivent_core.managers.resource_managers import texture_manager
from kivent_core.gameworld import GameWorld


class AttractorGame(Widget):
    def __init__(self, **kwargs):
        super(AttractorGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld([], callback=self.initGame)

    def initGame(self):
        pass
