import os
import json
import random

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
from kivy.graphics import Rectangle

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
from AttractorSystem import AttractorSystem

# Custom widgets
from TouchedTextBox import TouchedTextBox
from CircularButton import CircularButton
from BetterButton import BetterButton


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
    current_level = 0
    dd = None
    clock = None

    wall_sound = -1
    change_sound = -1
    unpause_button = None


    def __init__(self, **kwargs):
        super(AttractorGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(['cymunk_physics',
                                       'position',
                                       'rotate',
                                       'rotate_renderer',
                                       'bg_renderer',
                                       'mid_renderer',
                                       'animation',
                                       'play_camera',
                                       'finish',
                                       'pole_changer',
                                       'attractor',
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
        self.load_sounds()
        self.load_music()

        self.populate_level_select_menu()

        self.entity_factory = EntityFactory(self.gameworld, self.ids.cymunk_physics)
        self.editor = self.gameworld.system_manager['editor']
        self.editor.screen = self.ids.gamescreenmanager.ids.editor_screen

        # self.load_level('test')
        self.ids.play_camera.focus_entity = True
        self.ids.play_camera.entity_to_focus = self.attractor_id
        self.ids.cymunk_physics.collision_slop = 2
        # self.gameworld.system_manager['cymunk_physics'].damping = 0.5

        physics = self.ids.cymunk_physics
        physics.add_collision_handler(1, 2, self.membrane_solver)
        physics.add_collision_handler(1, 1, self.wall_solver)

        self.update_track('title')

    def _keyboard_closed(self):
        pass

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.editor.handle_key_down(keycode[1])

    def _on_keyboard_up(self, keyboard, keycode):
        pass

    def membrane_solver(self, space, arbiter):
        attractor_id = arbiter.shapes[0].body.data
        membrane_id = arbiter.shapes[1].body.data

        attractor = self.gameworld.entities[attractor_id]
        membrane = self.gameworld.entities[membrane_id]

        if attractor.charge.charge == membrane.charge.charge:
            return False
        else:
            # self.gameworld.managers['sound_manager'].play_direct(self.sound, 1.0)
            return True

    def wall_solver(self, space, arbiter):
        # self.play_sound(self.wall_sound, 0.5)
        return True

    def setup_states(self):
        self.gameworld.add_state(state_name='menu',
                                 systems_added=[],
                                 systems_removed=[],
                                 systems_paused=['position',
                                                 'rotate',
                                                 'rotate_renderer',
                                                 'bg_renderer',
                                                 'mid_renderer',
                                                 'animation',
                                                 'cymunk_physics',
                                                 'play_camera',
                                                 'pole_changer',
                                                 'finish',
                                                 'attractor',
                                                 'charge'],
                                 systems_unpaused=[],
                                 screenmanager_screen='menu_screen')
        self.gameworld.add_state(state_name='play',
                                 systems_added=['position',
                                                'rotate',
                                                'rotate_renderer',
                                                'bg_renderer',
                                                'mid_renderer',
                                                'animation',
                                                'cymunk_physics',
                                                'play_camera',
                                                'pole_changer',
                                                'finish',
                                                'attractor',
                                                'charge'],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=['position',
                                                   'rotate',
                                                   'rotate_renderer',
                                                   'bg_renderer',
                                                   'mid_renderer',
                                                   'animation',
                                                   'cymunk_physics',
                                                   'play_camera',
                                                   'pole_changer',
                                                   'finish',
                                                   'attractor',
                                                   'charge'],
                                 screenmanager_screen='play_screen')
        self.gameworld.add_state(state_name='editor',
                                 systems_added=['position',
                                                'rotate',
                                                'rotate_renderer',
                                                'bg_renderer',
                                                'mid_renderer',
                                                'animation',
                                                'cymunk_physics',
                                                'play_camera',
                                                'pole_changer',
                                                'finish',
                                                'attractor',
                                                'charge'],
                                 systems_removed=[],
                                 systems_paused=[],
                                 systems_unpaused=['position',
                                                   'rotate',
                                                   'rotate_renderer',
                                                   'bg_renderer',
                                                   'mid_renderer',
                                                   'animation',
                                                   'cymunk_physics',
                                                   'play_camera',
                                                   'pole_changer',
                                                   'finish',
                                                   'attractor',
                                                   'charge'],
                                 screenmanager_screen='editor_screen')
        self.gameworld.add_state(state_name='finish',
                                 systems_added=[],
                                 systems_removed=[],
                                 systems_paused=['position',
                                                 'rotate',
                                                 'rotate_renderer',
                                                 'bg_renderer',
                                                 'mid_renderer',
                                                 'animation',
                                                 'cymunk_physics',
                                                 'play_camera',
                                                 'pole_changer',
                                                 'finish',
                                                 'attractor',
                                                 'charge'],
                                 systems_unpaused=[],
                                 screenmanager_screen='finish_screen')

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

    def load_sounds(self):
        manager = self.gameworld.managers['sound_manager']
        with open('resources/sfx/sounds.json') as j_file:
            data = json.load(j_file)

        for sound in data['sounds']:
            if sound['name'] == 'wall_sound':
                self.wall_sound = manager.load_sound(sound['name'], sound['source'])
            elif sound['name'] == 'change_sound':
                self.change_sound = manager.load_sound(sound['name'], sound['source'])

    def load_music(self):
        manager = self.gameworld.managers['sound_manager']
        for root, dirs, files in os.walk("resources/music/"):
            for music_file in files:
                manager.load_music(music_file.split('.')[0],
                                   os.path.join(root, music_file))

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

        elif self.gameworld.state == 'play' and self.unpause_button is None:
            menu = self.ids.gamescreenmanager.ids.menu_screen
            self.unpause_button = BetterButton(text='Unpause')
            self.unpause_button.bind(on_release=self.go_to_play_screen)
            menu.ids.button_container.add_widget(self.unpause_button)
        else:
            menu = self.ids.gamescreenmanager.ids.menu_screen
            try:
                menu.ids.button_container.remove_widget(self.unpause_button)
            except AttributeError:
                pass

        self.gameworld.gamescreenmanager.transition.direction = 'left'
        self.gameworld.state = 'menu'

    def open_level_select_menu(self):
        scr = self.ids.gamescreenmanager.ids.menu_screen
        buttons = scr.level_buttons

        scr.scroll_container.x = scr.width
        anim = Animation(x=scr.width - scr.scroll_container.width, duration=0.25)
        anim.start(scr.scroll_container)

    def populate_level_select_menu(self):
        h_int = 40
        h = str(h_int) + 'dp'

        scr = self.ids.gamescreenmanager.ids.menu_screen
        buttons = scr.level_buttons

        buttons.add_widget(Label(text='[b]Magnet[/b]', markup=True))
        buttons.add_widget(Label())
        for i in range(1, 5):
            button = BetterButton(text=str(i),
                                  size_hint_y=None,
                                  height=h)
            button.bind(on_release=self.play_level)
            buttons.add_widget(button)

        buttons.add_widget(Label(text='[b]Rotator[/b]', markup=True))
        buttons.add_widget(Label())
        for i in range(5, 9):
            button = BetterButton(text=str(i),
                                    size_hint_y=None,
                                    height=h)
            button.bind(on_release=self.play_level)
            buttons.add_widget(button)

        buttons.add_widget(Label(text='[b]Membrane[/b]', markup=True))
        buttons.add_widget(Label())
        for i in range(9, 13):
            button = BetterButton(text=str(i),
                                    size_hint_y=None,
                                    height=h)
            button.bind(on_release=self.play_level)
            buttons.add_widget(button)

        buttons.add_widget(Label(text='[b]Changer[/b]', markup=True))
        buttons.add_widget(Label())
        for i in range(13, 17):
            button = BetterButton(text=str(i),
                                    size_hint_y=None,
                                    height=h)
            button.bind(on_release=self.play_level)
            buttons.add_widget(button)

        buttons.size_y = len(buttons.children) * h_int + h_int/2
        buttons.bind(minimum_height=buttons.setter('height'))

    def go_to_play_screen(self, *args):
        self.gameworld.state = 'play'

    def go_to_editor_screen(self):
        if platform != 'android':
            self.toggle_level_editor()

    def change_attractor_charge(self, button, change_to):
        button.background_color[3] = 0.15
        c = button.background_color
        anim = Animation(background_color=[c[0], c[1], c[2], 0], d=0.5, t='out_circ')
        anim.start(button)

        attractor = self.gameworld.entities[self.attractor_id]

        attractor.attractor.to_change = change_to
        attractor.charge.charge = change_to

        self.editor.level.stats.changes += 1
        self.ids.gamescreenmanager.play_screen.changes.text = \
            str(self.editor.level.stats.changes) + ' / ' + \
            str(self.editor.level.stats.ideal_changes)

        self.play_sound(self.change_sound, 2.0)

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
            self.ids.play_camera.entity_to_focus = self.attractor_id
            self.editor.remove_anchors()

        else:
            self.load_level('level1')
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
            self.editor.asset_id = -1
            self.editor.entity_to_place = ''

        if not self.editor.deleting:
            self.editor.entity_to_place = instance.text
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
            if name == 'attractor':
                continue

            level_data['entities'].append({'name': name,
                                           'x': point.x,
                                           'y': point.y,
                                           'rotation': rotation})

        if level.background is not None:
            source = 'resources' + level.background.source.split('resources')[1]
            level_data['background'] = {'x': level.background.pos[0],
                                        'y': level.background.pos[1],
                                        'w': level.background.size[0],
                                        'h': level.background.size[1],
                                        'source': source}

        if level.background2 is not None:
            source = 'resources' + level.background2.source.split('resources')[1]
            level_data['background2'] = {'x': level.background2.pos[0],
                                         'y': level.background2.pos[1],
                                         'w': level.background2.size[0],
                                         'h': level.background2.size[1],
                                         'source': source}

        level_data['ideal_time'] = self.editor.level.stats.ideal_time
        level_data['ideal_changes'] = self.editor.level.stats.ideal_changes
        level_data['attractor_pos'] = (int(self.editor.screen.ids.attractor_pos_x.text),
                                       int(self.editor.screen.ids.attractor_pos_y.text))

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
        self.ids.play_camera.canvas.before.clear()
        self.ids.play_camera.canvas.after.clear()

        # Try to get background from level
        try:
            with self.ids.play_camera.canvas.before:
                self.editor.level.background = Rectangle(pos=(level_data['background']['x'],
                                                              level_data['background']['y']),
                                                         size=(level_data['background']['w'],
                                                               level_data['background']['h']),
                                                         source=level_data['background']['source'])
            with self.ids.play_camera.canvas.before:
                self.editor.level.background2 = Rectangle(pos=(level_data['background2']['x'],
                                                               level_data['background2']['y']),
                                                          size=(level_data['background2']['w'],
                                                                level_data['background2']['h']),
                                                          source=level_data['background2']['source'])
        except KeyError:
            pass

        # Try to get ideal time and changes from level
        try:
            self.editor.level.stats.ideal_time = level_data['ideal_time']
            self.editor.level.stats.ideal_changes = level_data['ideal_changes']
        except KeyError:
            self.editor.level.stats.ideal_time = 0
            self.editor.level.stats.ideal_changes = 0

        # Try to get music track from level
        try:
            track = level_data['track']
        except KeyError:
            track = 'daflute'

        # Try to get attractor position from level
        try:
            pos = level_data['attractor_pos']
            attractor_pos = (int(pos[0]), int(pos[1]))
        except KeyError:
            attractor_pos = (200, 200)

        self.editor.level.attractor_pos = attractor_pos

        xbox = self.gameworld.gamescreenmanager.ids.editor_screen.ids.attractor_pos_x
        ybox = self.gameworld.gamescreenmanager.ids.editor_screen.ids.attractor_pos_y
        xbox.text = str(attractor_pos[0])
        ybox.text = str(attractor_pos[1])

        # Order entities
        finish = None
        corners= []
        other = []
        changers = []
        for ent in level_data['entities']:
            name = ent['name']
            if name == 'finish':
                finish = [ent]
            elif name == 'wall_corner':
                corners.append(ent)
            elif 'changer' in name:
                changers.append(ent)
            else:
                other.append(ent)

        try:
            ents = changers + other + corners + finish
        except TypeError:
            ents = level_data['entities']

        for ent in ents:
            name = ent['name']
            x = ent['x']
            y = ent['y']
            rot = ent['rotation']

            ids = self.entity_factory.create_entity_at(name, x, y, rot)
            self.editor.level.add_entity(name, x, y, rot, ids)

        self.create_attractor(attractor_pos)

        if self.gameworld.state == 'editor':
            self.ids.play_camera.focus_entity = False
            self.editor.redraw_anchors()
        else:
            self.ids.play_camera.focus_entity = True

        self.editor.level.stats.timer = 0
        self.editor.level.stats.changes = 0
        self.ids.gamescreenmanager.play_screen.time.text = '0 / ' + \
                str(self.editor.level.stats.ideal_time)
        self.ids.gamescreenmanager.play_screen.changes.text = '0 / ' + \
                str(self.editor.level.stats.ideal_changes)

        if self.clock is None:
            self.clock = Clock.schedule_interval(self.update_timer, 1)

        self.update_track(track)

    def finish_level(self):
        self.gameworld.state = 'finish'
        screen = self.ids.gamescreenmanager.ids.finish_screen

        screen.ids.time.text = str(int(round(self.editor.level.stats.timer))) + \
            ' / ' + str(self.editor.level.stats.ideal_time)

        screen.ids.changes.text = str(self.editor.level.stats.changes) + ' / ' + \
            str(self.editor.level.stats.ideal_changes)

        # self.fade_out_track()

    def clear_level(self):
        self.gameworld.clear_entities()
        self.ids.play_camera.canvas.before.clear()
        self.editor.level.clear()

    def create_attractor(self, pos):
        self.attractor_id = self.entity_factory.create_entity_at('attractor',
                                                                 pos[0],
                                                                 pos[1],
                                                                 0)
        self.editor.level.add_entity('attractor',
                                     pos[0],
                                     pos[1],
                                     0,
                                     self.attractor_id)

    def reset_attractor(self):
        self.play_sound(self.change_sound, 2.0)

        attractor = self.gameworld.entities[self.attractor_id]
        attractor.attractor.to_change = 'r'
        attractor.charge.charge = 'n'
        attractor.cymunk_physics.body.velocity = (0, 0)

        Clock.schedule_once(lambda dt: self.return_attractor_to_start_pos(), 0.5)

    def return_attractor_to_start_pos(self):
        attractor = self.gameworld.entities[self.attractor_id]

        attractor.position.pos = self.editor.level.attractor_pos
        attractor.cymunk_physics.body.position = self.editor.level.attractor_pos
        attractor.cymunk_physics.body.velocity = (0, 0)

        attractor.charge.charge = 'n'
        attractor.attractor.to_change = 'n'
        # self.play_sound(self.reset_sound, 1.0)


    def update_timer(self, dt):
        self.editor.level.stats.timer += dt
        self.ids.gamescreenmanager.play_screen.time.text = \
            str(int(round(self.editor.level.stats.timer))) + \
            ' / ' + str(self.editor.level.stats.ideal_time)
    def go_to_next_level(self):
        self.current_level = self.current_level + 1
        self.load_level('level' + str(self.current_level))

        self.gameworld.state = 'play'

    def update_track(self, name):
        manager = self.gameworld.managers['sound_manager']
        if manager.current_track != name:
            self.fade_out_track()
            Clock.schedule_once(lambda dt: self.fade_in_track(name), 3)

    def fade_in_track(self, name):
        manager = self.gameworld.managers['sound_manager']
        manager.music_volume = 1.0
        manager.play_track(name)

    def fade_out_track(self):
        manager = self.gameworld.managers['sound_manager']
        anim = Animation(music_volume=0.0, duration=2)
        anim.start(manager)

    def play_sound(self, direct_num, vol=1.0):
        self.gameworld.managers['sound_manager'].play_direct(direct_num, vol)
