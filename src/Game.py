import os
import json
from math import pi

# Kivy visuals
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

# Properties
from kivy.properties import NumericProperty

# Core
import kivent_core
import kivent_cymunk

# from cymunk import Body
# from cymunk import PivotJoint

# Managers
from kivent_core.managers.resource_managers import texture_manager

from EntityFactory import EntityFactory
from ChargeSystem import ChargeSystem, ChargeComponent
from TouchedTextBox import TouchedTextBox
# from IconButton import IconButton
from Level import Level


# Load all .png in resources/png
png_list = []
png_source_list = []
for root, dirs, files in os.walk("resources/png"):
    for asset in files:
        if '.atlas' in asset:
            texture_manager.load_atlas(os.path.join(root, asset))

        if '.png' in asset:
            texture_manager.load_image(os.path.join(root, asset))

            png_list.append(asset)
            png_source_list.append(os.path.join(root, asset))


class AttractorGame(Widget):
    attractor_id = NumericProperty(-1)

    level_editor_deleting = False
    level_editor_entity_to_place = ''
    level_editor_rotate = 0
    level_editor_level = Level()

    def __init__(self, **kwargs):
        super(AttractorGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(['cymunk_physics',
                                       'position',
                                       'rotate',
                                       'rotate_renderer',
                                       'play_camera',
                                       'charge'],
                                      callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.gameworld.state = 'menu'
        self.load_models()

        self.entity_factory = EntityFactory(self.gameworld.init_entity)
        self.clear_level()

    def setup_states(self):
        self.gameworld.add_state(state_name='menu',
                                 systems_added=['rotate_renderer',
                                                'charge'],
                                 systems_removed=['position',
                                                  'rotate',
                                                  'cymunk_physics',
                                                  'play_camera'],
                                 systems_paused=[],
                                 systems_unpaused=['rotate_renderer',
                                                   'charge'],
                                 screenmanager_screen='menu_screen')
        self.gameworld.add_state(state_name='play',
                                 systems_added=['position',
                                                'rotate',
                                                'rotate_renderer',
                                                'cymunk_physics',
                                                'play_camera',
                                                'charge'],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=['rotate_renderer',
                                                   'position',
                                                   'rotate',
                                                   'cymunk_physics',
                                                   'play_camera',
                                                   'charge'],
                                 screenmanager_screen='play_screen')
        self.gameworld.add_state(state_name='editor',
                                 systems_added=['position',
                                                'rotate',
                                                'rotate_renderer',
                                                'cymunk_physics',
                                                'play_camera',
                                                'charge'],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=['rotate_renderer',
                                                   'position',
                                                   'rotate',
                                                   'cymunk_physics',
                                                   'play_camera',
                                                   'charge'],
                                 screenmanager_screen='editor_screen')

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
            tex_key = texture_manager.get_texkey_from_name(asset_name)
            uv = texture_manager.get_uvs(tex_key)
            uv = list((uv[0], uv[3], uv[2], uv[1]))
            model = model_manager.models[asset_name]
            model.set_textured_rectangle(width, height, uv)

    def create_entities(self):
        self.attractor_id = self.entity_factory.create_entity_at('attractor', 100, 100)
        # attractor = self.gameworld.entities[self.attractor_id]

        # Debug moving stuff
        # self.moving_to = Body('INF', 'INF')
        # self.moving_to.position = attractor.position.pos
        # joint = PivotJoint(self.moving_to, attractor.cymunk_physics.body, (0, 0), (0, 0))
        # joint.max_force = 5000.
        # joint.max_bias = 5000.
        # self.ids.cymunk_physics.space.add_constraint(joint)
        #

        # self.entity_factory.create_entity_at('posipole', 0, 100)

    def go_to_play_screen(self):
        self.gameworld.state = 'play'

    def go_to_editor_screen(self):
        self.toggle_level_editor()

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
        attractor.rotate_renderer.texture_key = new_texture
        attractor.charge.charge = change_to

    def on_touch_down(self, touch):
        if super(AttractorGame, self).on_touch_down(touch):
            return True

        state = self.gameworld.state

        if state == 'editor':
            if self.level_editor_deleting:
                pass

            else:
                if self.level_editor_entity_to_place == '':
                    return

                cam_pos = self.ids.play_camera.camera_pos
                scale = self.ids.play_camera.camera_scale
                pos = (touch.pos[0] * scale - cam_pos[0], touch.pos[1] * scale - cam_pos[1])

                grid = self.ids.gamescreenmanager.ids.editor_screen.ids.grid

                if not isinstance(grid, int):
                    on_grid_x = int(round(pos[0]/10) * 10)
                    on_grid_y = int(round(pos[1]/10) * 10)

                else:
                    on_grid_x = int(round(pos[0]/grid) * grid)
                    on_grid_y = int(round(pos[1]/grid) * grid)

                self.entity_factory.create_entity_at(self.level_editor_entity_to_place,
                                                     on_grid_x,
                                                     on_grid_y,
                                                     self.level_editor_rotate)
                self.level_editor_level.add_entity(self.level_editor_entity_to_place,
                                                   on_grid_x,
                                                   on_grid_y,
                                                   self.level_editor_rotate)
                self.level_editor_entity_to_place = ''

        # For debug use only
        elif state == 'play':
            b = self.moving_to
            cam_pos = self.ids.play_camera.camera_pos
            scale = self.ids.play_camera.camera_scale
            pos = (touch.pos[0] * scale - cam_pos[0], touch.pos[1] * scale - cam_pos[1])

            b.position = pos

            bodies = self.ids.cymunk_physics.space.bodies
            if b not in bodies:
                self.ids.cymunk_physics.space.add_body(b)

    def toggle_editor_deleting(self):
        self.level_editor_deleting = not self.level_editor_deleting

    def toggle_level_editor(self):
        if self.gameworld.state == 'editor':
            self.gameworld.state = 'play'

            self.ids.play_camera.focus_entity = True
            self.ids.rotate_renderer.gameview = 'play_camera'

        else:
            self.gameworld.state = 'editor'
            self.ids.play_camera.focus_entity = False

            self.dd = DropDown()

            names = self.entity_factory.get_entity_names()
            for ent_name in names:
                butt = Button(text=ent_name,
                              size_hint_y=None,
                              width=150,
                              height=40)
                butt.bind(on_release=self.grab_entity_to_place)
                self.dd.add_widget(butt)

            main_butt = Button(text='Select',
                               size_hint=(None, None),
                               width=150,
                               height=30)

            main_butt.bind(on_release=self.dd.open)
            self.dd.bind(on_select=self.dd.dismiss)
            self.ids.gamescreenmanager.ids.editor_screen.ids.ui.add_widget(main_butt)

    def grab_entity_to_place(self, instance):
        self.dd.dismiss()
        self.level_editor_entity_to_place = instance.text

    def save_level(self):
        level = self.level_editor_level
        level_file_name = self.ids.gamescreenmanager.ids.editor_screen.ids.level_name.text

        if level_file_name == '':
            return

        level_data = {'entities': []}

        while not level.empty():
            name, point, rotation = level.pop_entity()
            level_data['entities'].append({'name': name,
                                           'x': point.x,
                                           'y': point.y,
                                           'rotation': rotation})

        if not len(level_data['entities']) == 0:
            with open('resources/levels/' + level_file_name + '.json', 'w', encoding='utf-8') as f:
                json.dump(level_data, f, indent=2)

    def load_level(self):
        level_file_name = self.ids.gamescreenmanager.ids.editor_screen.ids.level_name.text

        if level_file_name == '':
            return

        self.clear_level()

        with open('resources/levels/' + level_file_name + '.json', 'r', encoding='utf-8') as f:
            level_data = json.load(f)

        if 'entities' not in level_data:
            return

        for ent in level_data['entities']:
            name = ent['name']
            x = ent['x']
            y = ent['y']
            rot = ent['rotation']

            self.entity_factory.create_entity_at(name, x, y, rot)
            self.level_editor_level.add_entity(name, x, y, rot)

    def clear_level(self):
        self.gameworld.clear_entities()
        self.attractor_id = self.entity_factory.create_entity_at('attractor',
                                                                 100,
                                                                 100,
                                                                 0)
        self.level_editor_level.add_entity('attractor',
                                           100,
                                           100,
                                           0)
        self.level_editor_level.clear()
