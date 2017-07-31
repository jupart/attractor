import os
import json

from kivy.utils import platform
from kivy.clock import Clock

# Kivy visuals
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.screenmanager import FadeTransition

# Properties
from kivy.properties import NumericProperty

# Core
import kivent_core
import kivent_cymunk

# Plyer
if platform == 'android' or platform == 'ios':
    import plyer

# Managers
from kivent_core.managers.resource_managers import texture_manager

from EntityFactory import EntityFactory
from LevelEditor import LevelEditorSystem
from ChargeSystem import ChargeSystem
from FinishSystem import FinishSystem
from PoleChangerSystem import PoleChangerSystem

# Custom widgets
from TouchedTextBox import TouchedTextBox
from CircularButton import CircularButton
from MaterialButton import MaterialButton


# Load all .png in resources/png
png_list = []
png_source_list = []
for root, dirs, files in os.walk("resources/png"):
    for asset in files:
        if '.atlas' in asset:
            texture_manager.load_atlas(os.path.join(root, asset))
            png_list.append('attractor_negative_idle_00.png')
            png_list.append('attractor_negative_idle_01.png')
            png_list.append('attractor_negative_idle_02.png')
            png_list.append('attractor_negative_idle_03.png')
            png_list.append('attractor_negative_idle_04.png')
            png_list.append('attractor_negative_idle_05.png')
            png_list.append('attractor_negative_idle_06.png')
            png_list.append('attractor_negative_idle_07.png')
            png_list.append('attractor_negative_idle_08.png')
            png_list.append('attractor_negative_idle_09.png')
            png_list.append('attractor_negative_idle_10.png')
            png_list.append('attractor_negative_idle_11.png')

            png_list.append('attractor_positive_idle_00.png')
            png_list.append('attractor_positive_idle_01.png')
            png_list.append('attractor_positive_idle_02.png')
            png_list.append('attractor_positive_idle_03.png')
            png_list.append('attractor_positive_idle_04.png')
            png_list.append('attractor_positive_idle_05.png')
            png_list.append('attractor_positive_idle_06.png')
            png_list.append('attractor_positive_idle_07.png')
            png_list.append('attractor_positive_idle_08.png')
            png_list.append('attractor_positive_idle_09.png')
            png_list.append('attractor_positive_idle_10.png')
            png_list.append('attractor_positive_idle_11.png')

        if '.png' in asset:
            texture_manager.load_image(os.path.join(root, asset))

            png_list.append(asset)
            png_source_list.append(os.path.join(root, asset))


class AttractorGame(Widget):
    attractor_id = NumericProperty(-1)
    current_level = 0
    dd = None

    def __init__(self, **kwargs):
        super(AttractorGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(['cymunk_physics',
                                       'position',
                                       'rotate',
                                       'animation',
                                       'rotate_renderer',
                                       'play_camera',
                                       'finish',
                                       'pole_changer',
                                       'charge'],
                                      callback=self.init_game)

    def init_game(self):
        if not(platform == 'android' or platform == 'ios'):
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            self._keyboard.bind(on_key_up=self._on_keyboard_up)

        self.setup_states()
        self.gameworld.state = 'menu'
        self.load_models()
        self.load_animations()

        self.entity_factory = EntityFactory(self.gameworld, self.ids.cymunk_physics)
        self.editor = self.gameworld.system_manager['editor']
        self.editor.screen = self.ids.gamescreenmanager.ids.editor_screen
        self.clear_level()

        self.load_level('test')
        self.ids.play_camera.focus_entity = True
        self.ids.play_camera.entity_to_focus = self.attractor_id
        self.ids.cymunk_physics.collision_slop = 2
        # self.gameworld.system_manager['cymunk_physics'].damping = 0.5

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.add_collision_handler(1, 2, self.membrane_solver)

        if platform == 'android' or platform == 'ios':
            if plyer.vibrator.exists:
                plyer.vibrator.vibrate(0.05)

    def _keyboard_closed(self):
        pass

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.editor.handle_key_down(keycode[1])

    def _on_keyboard_up(self, keyboard, keycode):
        pass

    def membrane_solver(self, space, arbiter):
        attractor_id = arbiter.shapes[0].body.data
        membrane_id = arbiter.shapes[0].body.data

        attractor = self.gameworld.entities[attractor_id]
        membrane = self.gameworld.entities[membrane_id]

        if attractor.charge.charge == membrane.charge.charge:
            return False
        else:
            return True

    def setup_states(self):
        self.gameworld.add_state(state_name='menu',
                                 systems_added=[],
                                 systems_removed=[],
                                 systems_paused=['position',
                                                 'rotate',
                                                 'animation',
                                                 'rotate_renderer',
                                                 'cymunk_physics',
                                                 'play_camera',
                                                 'pole_changer',
                                                 'finish',
                                                 'charge'],
                                 systems_unpaused=[],
                                 screenmanager_screen='menu_screen')
        self.gameworld.add_state(state_name='play',
                                 systems_added=['position',
                                                'rotate',
                                                'animation',
                                                'rotate_renderer',
                                                'cymunk_physics',
                                                'play_camera',
                                                'pole_changer',
                                                'finish',
                                                'charge'],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=['rotate_renderer',
                                                   'position',
                                                   'rotate',
                                                   'animation',
                                                   'cymunk_physics',
                                                   'play_camera',
                                                   'pole_changer',
                                                   'finish',
                                                   'charge'],
                                 screenmanager_screen='play_screen')
        self.gameworld.add_state(state_name='editor',
                                 systems_added=['position',
                                                'rotate',
                                                'animation',
                                                'rotate_renderer',
                                                'cymunk_physics',
                                                'play_camera',
                                                'pole_changer',
                                                'finish',
                                                'charge'],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=['rotate_renderer',
                                                   'position',
                                                   'rotate',
                                                   'animation',
                                                   'cymunk_physics',
                                                   'play_camera',
                                                   'pole_changer',
                                                   'finish',
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

    def load_animations(self):
        manager = self.gameworld.animation_manager
        with open('resources/animations.json') as j_file:
            data = json.load(j_file)

        for anim in data['animations']:
            animation_frames = []

            for f in anim['frames']:
                animation_frames.append({
                    'texture': f['frame'],
                    'model': f['frame'],
                    'duration': anim['duration']})

            manager.load_animation(anim['name'], len(animation_frames), animation_frames)

    def create_entities(self):
        self.attractor_id = self.entity_factory.create_entity_at('attractor', 200, 200)
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

    def go_to_menu_screen(self):
        if self.gameworld.state == 'editor':
            self.toggle_level_editor()
            if self.editor.asset_id != -1:
                self.gameworld.remove_entity(self.editor.asset_id)
                self.editor.asset_id = -1
        self.gameworld.gamescreenmanager.transition.direction = 'right'
        self.gameworld.state = 'menu'

    def open_level_select_menu(self):
        h_int = 40
        h = str(h_int) + 'dp'
        z1 = 2
        z2 = 1

        scr = self.ids.gamescreenmanager.ids.menu_screen
        buttons = scr.level_buttons

        if buttons.children == []:
            # for root, dirs, files in os.walk("resources/levels"):
                # for level in files:
                    # button = Button(text=level[:-5].replace('level', ''),
                                    # size_hint_y=None,
                                    # height=h)
                    # button.bind(on_release=self.play_level)
                    # buttons.add_widget(button)
            buttons.add_widget(Label(text='[b]Magnet[/b]', markup=True))
            buttons.add_widget(Label())
            for i in range(1, 5):
                button = MaterialButton(text=str(i),
                                        size_hint_y=None,
                                        elevation=z1,
                                        raised_elevation=z1,
                                        pressed_elevation=z2,
                                        height=h)
                button.bind(on_release=self.play_level)
                buttons.add_widget(button)

            buttons.add_widget(Label(text='[b]Rotator[/b]', markup=True))
            buttons.add_widget(Label())
            for i in range(5, 9):
                button = MaterialButton(text=str(i),
                                        size_hint_y=None,
                                        elevation=z1,
                                        raised_elevation=z1,
                                        pressed_elevation=z2,
                                        height=h)
                button.bind(on_release=self.play_level)
                buttons.add_widget(button)

            buttons.add_widget(Label(text='[b]Changer[/b]', markup=True))
            buttons.add_widget(Label())
            for i in range(9, 13):
                button = MaterialButton(text=str(i),
                                        size_hint_y=None,
                                        elevation=z1,
                                        raised_elevation=z1,
                                        pressed_elevation=z2,
                                        height=h)
                button.bind(on_release=self.play_level)
                buttons.add_widget(button)

            buttons.add_widget(Label(text='[b]Membrane[/b]', markup=True))
            buttons.add_widget(Label())
            for i in range(13, 17):
                button = MaterialButton(text=str(i),
                                        size_hint_y=None,
                                        elevation=z1,
                                        raised_elevation=z1,
                                        pressed_elevation=z2,
                                        height=h)
                button.bind(on_release=self.play_level)
                buttons.add_widget(button)

        buttons.size_y = len(buttons.children) * h_int + h_int/2
        buttons.bind(minimum_height=buttons.setter('height'))

        scr.scroll_container.x = scr.width
        anim = Animation(x=scr.width - scr.scroll_container.width, duration=0.25)
        anim.start(scr.scroll_container)

    def go_to_play_screen(self):
        self.gameworld.state = 'play'

    def go_to_editor_screen(self):
        self.toggle_level_editor()

    def change_attractor_charge(self, button, change_to):
        button.background_color[3] = 0.1
        c = button.background_color
        anim = Animation(background_color=[c[0], c[1], c[2], 0], d=0.5, t='out_circ')
        anim.start(button)

        if change_to != '+' and change_to != '-' and change_to != 'n':
            return

        attractor = self.gameworld.entities[self.attractor_id]

        new_anim = 'attractor_neutral_idle'
        if change_to == '+':
            new_anim = 'attractor_positive_idle'
        elif change_to == '-':
            new_anim = 'attractor_negative_idle'
        else:
            pass

        attractor.animation.animation = new_anim
        attractor.charge.charge = change_to

        if platform == 'android' or platform == 'ios':
            if plyer.vibrator.exists:
                plyer.vibrator.vibrate(0.05)

    def on_touch_down(self, touch):
        if super(AttractorGame, self).on_touch_down(touch):
            return True

        state = self.gameworld.state

        if state == 'editor':
            self.editor.handle_click(touch)

        # cam = self.ids.play_camera

        # cam_pos = cam.camera_pos
        # scale = cam.camera_scale
        # pos = (touch.pos[0] * scale - cam_pos[0], touch.pos[1] * scale - cam_pos[1])

        # For debug use only
        # elif state == 'play':
            # b = self.moving_to
            # b.position = pos

            # bodies = self.ids.cymunk_physics.space.bodies
            # if b not in bodies:
                # self.ids.cymunk_physics.space.add_body(b)

    def toggle_level_editor(self):
        if self.gameworld.state == 'editor':
            self.gameworld.state = 'menu'

            self.ids.play_camera.focus_entity = True
            self.ids.rotate_renderer.gameview = 'play_camera'
            self.ids.play_camera.entity_to_focus = self.attractor_id
            self.editor.remove_anchors()

        else:
            self.gameworld.state = 'editor'
            self.ids.play_camera.focus_entity = False
            self.editor.draw_anchors()

            if self.dd is None:
                self.dd = DropDown()

                names = self.entity_factory.get_entity_names()
                for ent_name in names:
                    butt = Button(text=ent_name,
                                  size_hint=(None, None),
                                  width=175,
                                  height=40)
                    butt.bind(on_release=self.grab_entity_to_place)
                    self.dd.add_widget(butt)

                main_butt = Button(text='Select',
                                   size_hint_x=None,
                                   width=175)

                main_butt.bind(on_release=self.dd.open)
                self.dd.bind(on_select=self.dd.dismiss)
                self.editor.screen.ids.ui.add_widget(main_butt)

    def grab_entity_to_place(self, instance):
        self.dd.dismiss()

        if self.editor.asset_id != -1:
            self.gameworld.remove_entity(self.editor.asset_id)

        self.editor.entity_to_place = instance.text

        if not self.editor.deleting:
            self.editor.asset_id = self.entity_factory.create_entity_at(
                        instance.text,
                        0,
                        0,
                        int(self.editor.screen.ids.rotation.text))

    def update_editor_rotation(self, r):
        asset_id = self.editor.asset_id
        name = self.editor.entity_to_place

        try:
            r_int = int(r)
        except ValueError:
            r_int = 0

        if asset_id != -1:
            self.gameworld.remove_entity(self.editor.asset_id)
            self.asset_id = self.entity_factory.create_entity_at(name, 0, 0, r_int)

    def save_level(self):
        level = self.editor.level
        level_file_name = self.editor.screen.ids.level_name.text

        if level_file_name == '':
            return

        level_data = {'entities': []}

        for name, point, rotation, ids in zip(level.names, level.points,
                                              level.rotations, level.ids):
            level_data['entities'].append({'name': name,
                                           'x': point.x,
                                           'y': point.y,
                                           'rotation': rotation})

        with open('resources/levels/' + level_file_name + '.json', 'wb') as f:
            json.dump(level_data, f, indent=2)

    def play_level(self, button):
        level_file_name = 'level' + button.text
        self.current_level = int(button.text)

        self.load_level(level_file_name)
        self.gameworld.gamescreenmanager.transition.direction = 'left'
        self.gameworld.state = 'play'

        Clock.schedule_once(lambda dt: self.hide_level_menu(), 1)

    def hide_level_menu(self):
        scr = self.ids.gamescreenmanager.ids.menu_screen
        scr.scroll_container.x = -scr.scroll_container.width

    def load_level(self, level_file_name=''):
        if level_file_name == '':
            level_file_name = self.editor.screen.ids.level_name.text
            if level_file_name == '':
                return
        path = 'resources/levels/' + level_file_name + '.json'
        if not os.path.isfile(path):
            return

        with open(path, 'rb') as f:
            level_data = json.load(f)
        if 'entities' not in level_data:
            return

        self.clear_level()

        # Order entities such that 'tiles' is always added first
        ordered_ents = []
        for ent in level_data['entities']:
            if ent['name'] != 'tiles':
                ordered_ents.append(ent)
            else:
                ordered_ents = [ent] + ordered_ents

        # Use those ordered entities to build the level
        for ent in ordered_ents:
            name = ent['name']
            x = ent['x']
            y = ent['y']
            rot = ent['rotation']

            ids = self.entity_factory.create_entity_at(name, x, y, rot)
            self.editor.level.add_entity(name, x, y, rot, ids)

    def finish_level(self):
        self.current_level = self.current_level + 1
        self.load_level('level' + str(self.current_level))

    def clear_level(self):
        self.gameworld.clear_entities()
        self.attractor_id = self.entity_factory.create_entity_at('attractor',
                                                                 200,
                                                                 200,
                                                                 0)
        self.editor.level.add_entity('attractor',
                                     200,
                                     200,
                                     0,
                                     self.attractor_id)
        self.editor.level.clear()

    def reset_attractor(self):
        attractor = self.gameworld.entities[self.attractor_id]
        attractor.position.pos = (200, 200)
        attractor.cymunk_physics.body.position = (200, 200)
        attractor.cymunk_physics.body.velocity = (0, 0)

        attractor.charge.charge = 'n'
        attractor.animation.animation = 'attractor_neutral_idle'
