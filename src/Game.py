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
        self.gameworld.init_gameworld([], callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.gameworld.state = 'menu'
        self.load_models()
        self.create_entities()

    def setup_states(self):
        self.gameworld.add_state(state_name='menu',
                                 systems_added=['rotate_renderer'],
                                 systems_removed=[],
                                 systems_paused=['position', 'camera'],
                                 systems_unpaused=['rotate_renderer'],
                                 screenmanager_screen='menu_screen')
        self.gameworld.add_state(state_name='play',
                                 systems_added=[],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=[],
                                 screenmanager_screen='play_screen')

    def load_models(self):
        pass

    def create_entities(self):
        pass

    def go_to_play_screen(self):
        self.gameworld.state = 'play'
