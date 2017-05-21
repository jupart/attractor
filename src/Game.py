from math import radians

# Kivy visuals
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager

# Properties
from kivy.properties import NumericProperty

# Core
import kivent_core
import kivent_cymunk

# Systems
from kivent_core.systems.position_systems import PositionSystem2D
from kivent_core.systems.rotate_systems import RotateSystem2D
from kivent_core.systems.renderers import RotateRenderer
from kivent_core.systems.gamesystem import GameSystem

# Managers
from kivent_core.managers.resource_managers import texture_manager
from kivent_core.gameworld import GameWorld


texture_manager.load_image('./resources/png/ball.png')


class AttractorGame(Widget):
    ball_id = NumericProperty(-1)

    def __init__(self, **kwargs):
        super(AttractorGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(['cymunk_physics',
                                       'position',
                                       'rotate',
                                       'rotate_renderer',
                                       'play_camera'], callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.gameworld.state = 'play'
        self.load_models()
        self.create_entities()

    def setup_states(self):
        self.gameworld.add_state(state_name='menu',
                                 systems_added=['rotate_renderer'],
                                 systems_removed=['position',
                                                  'rotate',
                                                  'cymunk_physics',
                                                  'play_camera',],
                                 systems_paused=[],
                                 systems_unpaused=['rotate_renderer'],
                                 screenmanager_screen='menu_screen')
        self.gameworld.add_state(state_name='play',
                                 systems_added=['position',
                                                'rotate',
                                                'rotate_renderer',
                                                'cymunk_physics',
                                                'play_camera',],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=['rotate_renderer',
                                                   'position',
                                                   'rotate',
                                                   'cymunk_physics',
                                                   'play_camera',],
                                 screenmanager_screen='play_screen')

    def load_models(self):
        model_manager = self.gameworld.model_manager
        model_manager.load_textured_rectangle('vertex_format_4f',
                                              12.,
                                              12.,
                                              'ball',
                                              'ball')

    def create_entities(self):
        gameview = self.gameworld.system_manager['play_camera']
        x = int(-gameview.camera_pos[0])
        y = int(-gameview.camera_pos[1])
        w = int(gameview.size[0])
        h = int(gameview.size[1])

        self.ball_id = self.createBall()
        ball = self.gameworld.entities[self.ball_id]

    def go_to_play_screen(self):
        self.gameworld.state = 'play'

    def createBall(self):
        shape = {'inner_radius': 0,
                 'outer_radius': 50,
                 'mass': 10,
                 'offset': (0, 0)}
        col_shape = {'shape_type': 'circle',
                     'elasticity': 0,
                     'collision_type': 1,
                     'shape_info': shape,
                     'friction': 1.0}
        col_shapes = [col_shape]
        physics = {'main_shape': 'circle',
                   'velocity': (0, 0),
                   'position': (100, 100),
                   'angle': 0,
                   'angular_velocity': 0,
                   'vel_limit': 100,
                   'ang_vel_limit': radians(200),
                   'mass': 10,
                   'moment': 1,
                   'col_shapes': col_shapes}
        components = {'position': (100, 100),
                      'rotate_renderer': {'texture': 'ball',
                                     'size': (100, 100),
                                     'model_key': 'ball',
                                     'render': True},
                      'cymunk_physics': physics,
                      'rotate': 0}
        order = ['position',
                 'rotate',
                 'rotate_renderer',
                 'cymunk_physics']
        return self.gameworld.init_entity(components, order)


