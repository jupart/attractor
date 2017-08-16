from math import radians

from kivy.app import App
from kivy.core.window import Window
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory
from kivy.graphics import Color, Line

from Level import Level


class LevelEditorSystem(GameSystem):
    def __init__(self, **kwargs):
        super(LevelEditorSystem, self).__init__(**kwargs)
        self.deleting = False
        self.rotate = 0
        self.level = Level()
        self.asset_id = -1
        self.screen = None
        self.entity_to_place = ''
        self.anchors = []

    def update(self, dt):
        if self.asset_id != -1:
            self.place_entity()

    def place_entity(self):
        app = App.get_running_app()
        cam_pos = app.game.ids.play_camera.camera_pos
        scale = app.game.ids.play_camera.camera_scale
        pos = (Window.mouse_pos[0] * scale - cam_pos[0],
               Window.mouse_pos[1] * scale - cam_pos[1])

        try:
            grid = int(self.screen.ids.grid.text)
        except ValueError:
            grid = 10

        try:
            r = int(self.screen.ids.rotation.text)
        except ValueError:
            r = 0

        on_grid_x = int(round(pos[0]/grid) * grid)
        on_grid_y = int(round(pos[1]/grid) * grid)

        draw_ent = self.gameworld.entities[self.asset_id]
        draw_ent.position.pos = (on_grid_x, on_grid_y)

        if hasattr(draw_ent, 'cymunk_physics'):
            draw_ent.cymunk_physics.body.position = draw_ent.position.pos
            draw_ent.cymunk_physics.body.angle = radians(r)

    def delete_at(self, pos):
        FLUFF = 20
        for i, point in enumerate(self.level.points):
            if ((pos[0] - FLUFF) < point.x) and ((point.x < pos[0] + FLUFF)) and \
                    ((pos[1] - FLUFF) < point.y) and ((point.y < pos[1] + FLUFF)):

                del self.level.names[i]
                del self.level.points[i]
                del self.level.rotations[i]

                ent_id = self.level.ids.pop(i)
                self.gameworld.remove_entity(ent_id)

    def handle_click(self, touch):
        app = App.get_running_app()
        cam = app.game.ids.play_camera

        cam_pos = cam.camera_pos
        scale = cam.camera_scale
        pos = (Window.mouse_pos[0] * scale - cam_pos[0],
               Window.mouse_pos[1] * scale - cam_pos[1])

        if touch.button == 'left':
            if self.deleting:
                self.delete_at(pos)

            else:
                if self.entity_to_place == '':
                    return

                try:
                    grid = int(self.screen.ids.grid.text)
                except ValueError:
                    grid = 10

                try:
                    r = int(self.screen.ids.rotation.text)
                except ValueError:
                    r = 0

                on_grid_x = int(round(pos[0]/grid) * grid)
                on_grid_y = int(round(pos[1]/grid) * grid)

                ids = app.game.entity_factory.create_entity_at(self.entity_to_place,
                                                               on_grid_x,
                                                               on_grid_y,
                                                               r)
                self.level.add_entity(self.entity_to_place,
                                      on_grid_x,
                                      on_grid_y,
                                      r,
                                      ids)

        elif touch.button == 'right':
            if self.asset_id != -1:
                self.entity_to_place = ''
                self.gameworld.remove_entity(self.asset_id)
                self.asset_id = -1

        elif touch.button == 'scrollup':
            cam.camera_scale = cam.camera_scale + 0.1
            cam.look_at(pos)

        elif touch.button == 'scrolldown':
            cam.camera_scale = cam.camera_scale - 0.1
            cam.look_at(pos)

        elif touch.button == 'middle':
            cam.look_at(pos)

    def handle_key_down(self, key):
        if key == 'r':
            self.rotate_entity_to_place()
        elif key == 'd':
            self.toggle_deleting()

    def toggle_deleting(self):
        if not self.deleting:
            button = self.screen.ids.delete
            if button.state == 'normal':
                button.state = 'down'

            self.deleting = True

            if self.asset_id != -1:
                self.gameworld.remove_entity(self.asset_id)
                self.asset_id = -1
                self.entity_to_place = ''

        else:
            button = self.screen.ids.delete
            if button.state == 'down':
                button.state = 'normal'

            self.deleting = False
            self.entity_to_place = ''
            self.asset_id = -1

    def rotate_entity_to_place(self):
        r = int(self.screen.ids.rotation.text)
        r += 45

        if r >= 360:
            r = r - 360

        self.screen.ids.rotation.text = str(r)

    def draw_anchors(self):
        anchors = self.anchors
        s = 4
        canvas = App.get_running_app().game.ids.play_camera.canvas
        with canvas.after:
            for p in self.level.points:
                x1, y1 = p.x - s, p.y
                x2, y2 = p.x + s, p.y
                x3, y3 = p.x, p.y
                x4, y4 = p.x, p.y + s
                x5, y5 = p.x, p.y - s
                Color(1, 1, 1, 1)
                anchors.append(Line(points=[x1, y1,
                                            x2, y2,
                                            x3, y3,
                                            x4, y4,
                                            x5, y5],
                                    width=1))

    def redraw_anchors(self):
        self.remove_anchors()
        self.draw_anchors()

    def remove_anchors(self):
        canvas = App.get_running_app().game.ids.play_camera.canvas
        for anchor in self.anchors:
            canvas.after.remove(anchor)
        del self.anchors[:]


Factory.register('LevelEditorSystem', cls=LevelEditorSystem)
