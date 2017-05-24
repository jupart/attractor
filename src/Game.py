# Kivy visuals
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager

# Properties
from kivy.properties import NumericProperty

# Core
import kivent_core
import kivent_cymunk

# Managers
from kivent_core.managers.resource_managers import texture_manager

from EntityFactory import EntityFactory


texture_manager.load_image('./resources/png/ball.png')


class AttractorGame(Widget):
    ball_id = NumericProperty(-1)

    def __init__(self, **kwargs):
        super(AttractorGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(['cymunk_physics',
                                       'position',
                                       'rotate',
                                       'rotate_renderer',
                                       'play_camera'],
                                      callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.gameworld.state = 'play'
        self.load_models()

        self.entity_factory = EntityFactory(self.gameworld.init_entity)
        self.create_entities()

    def setup_states(self):
        self.gameworld.add_state(state_name='menu',
                                 systems_added=['rotate_renderer'],
                                 systems_removed=['position',
                                                  'rotate',
                                                  'cymunk_physics',
                                                  'play_camera'],
                                 systems_paused=[],
                                 systems_unpaused=['rotate_renderer'],
                                 screenmanager_screen='menu_screen')
        self.gameworld.add_state(state_name='play',
                                 systems_added=['position',
                                                'rotate',
                                                'rotate_renderer',
                                                'cymunk_physics',
                                                'play_camera'],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=['rotate_renderer',
                                                   'position',
                                                   'rotate',
                                                   'cymunk_physics',
                                                   'play_camera'],
                                 screenmanager_screen='play_screen')

    def load_models(self):
        model_manager = self.gameworld.model_manager
        model_manager.load_textured_rectangle('vertex_format_4f',
                                              12.,
                                              12.,
                                              'ball',
                                              'ball')

    def create_entities(self):
        self.entity_factory.create_entity_at('ball', 100, 100)

    def go_to_play_screen(self):
        self.gameworld.state = 'play'

