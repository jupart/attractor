import os
# from pubsub import pub

# Kivy visuals
from kivy.uix.widget import Widget

# Properties
from kivy.properties import NumericProperty

# Core
import kivent_core
import kivent_cymunk

from cymunk import Body
from cymunk import PivotJoint

# Managers
from kivent_core.managers.resource_managers import texture_manager

from EntityFactory import EntityFactory
from ChargeSystem import ChargeSystem, ChargeComponent


png_list = []
png_source_list = []
for root, dirs, files in os.walk("resources/png"):
    load_using_load_image = True

    for asset in files:
        if '.atlas' in asset:
            load_using_load_image = False
            texture_manager.load_atlas(os.path.join(root, asset))

    for asset in files:
        if '.png' in asset:
            if load_using_load_image:
                texture_manager.load_image(os.path.join(root, asset))

            png_list.append(asset)
            png_source_list.append(os.path.join(root, asset))


class AttractorGame(Widget):
    attractor_id = NumericProperty(-1)

    def __init__(self, **kwargs):
        super(AttractorGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(['cymunk_physics',
                                       'position',
                                       'rotate',
                                       'renderer',
                                       'play_camera',
                                       'charge'],
                                      callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.load_models()

        self.entity_factory = EntityFactory(self.gameworld.init_entity)
        self.create_entities()
        self.go_to_play_screen()

    def setup_states(self):
        self.gameworld.add_state(state_name='menu',
                                 systems_added=['renderer',
                                                'charge'],
                                 systems_removed=['position',
                                                  'rotate',
                                                  'cymunk_physics',
                                                  'play_camera'],
                                 systems_paused=[],
                                 systems_unpaused=['renderer',
                                                   'charge'],
                                 screenmanager_screen='menu_screen')
        self.gameworld.add_state(state_name='play',
                                 systems_added=['position',
                                                'rotate',
                                                'renderer',
                                                'cymunk_physics',
                                                'play_camera',
                                                'charge'],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=['renderer',
                                                   'position',
                                                   'rotate',
                                                   'cymunk_physics',
                                                   'play_camera',
                                                   'charge'],
                                 screenmanager_screen='play_screen')

    def load_models(self):
        model_manager = self.gameworld.model_manager
        for png in png_list:
            asset_name = png[:-4]
            tex_key = texture_manager.get_texkey_from_name(asset_name)
            width, height = texture_manager.get_size(tex_key)
            model_manager.load_textured_rectangle('vertex_format_4f',
                                                  width, height,
                                                  asset_name,
                                                  asset_name)

    def create_entities(self):
        self.attractor_id = self.entity_factory.create_entity_at('attractor', 100, 100)
        attractor = self.gameworld.entities[self.attractor_id]

        self.moving_to = Body('INF', 'INF')
        self.moving_to.position = attractor.position.pos
        joint = PivotJoint(self.moving_to, attractor.cymunk_physics.body, (0, 0), (0, 0))
        joint.max_force = 5000.
        joint.max_bias = 5000.
        self.ids.cymunk_physics.space.add_constraint(joint)

        self.entity_factory.create_entity_at('dipole', 400, 400, 30)
        self.entity_factory.create_entity_at('wall', 1200, 400)

    def go_to_play_screen(self):
        self.gameworld.state = 'play'

    def change_attractor_charge(self, change_to):
        if change_to != '+' and change_to != '-' and change_to != 'n':
            return

        attractor = self.gameworld.entities[self.attractor_id]

        new_texture = 'attractor_neutral'
        if change_to == '+':
            new_texture = 'attractor_positive'
        elif change_to == '-':
            new_texture = 'attractor_negative'

        attractor.cymunk_physics.body.apply_impulse((-10, 0), (10, 0))
        attractor.renderer.texture_key = new_texture
        attractor.charge.charge = change_to

    def on_touch_down(self, touch):
        # This function is for debug use only
        if super(AttractorGame, self).on_touch_down(touch):
            return True

        state = self.gameworld.state

        if state == 'play':
            b = self.moving_to
            cam_pos = self.ids.play_camera.camera_pos
            scale = self.ids.play_camera.camera_scale
            pos = (touch.pos[0] * scale - cam_pos[0], touch.pos[1] * scale - cam_pos[1])

            b.position = pos

            bodies = self.ids.cymunk_physics.space.bodies
            if b not in bodies:
                self.ids.cymunk_physics.space.add_body(b)
