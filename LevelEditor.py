from math import radians

from kivy.app import App
from kivy.core.window import Window
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory

from Level import Level


class LevelEditorSystem(GameSystem):
    def __init__(self, **kwargs):
        super(LevelEditorSystem, self).__init__(**kwargs)
        self.deleting = False
        self.rotate = 0
        self.level = Level()
        self.asset_id = -1
        self.screen = None

    def update(self, dt):
        if self.asset_id != -1:
            self.place_entity()

    def place_entity(self):
        app = App.get_running_app()
        cam_pos = app.game.ids.play_camera.camera_pos
        scale = app.game.ids.play_camera.camera_scale
        pos = (Window.mouse_pos[0] * scale - cam_pos[0],
               Window.mouse_pos[1] * scale - cam_pos[1])

        grid = int(self.screen.ids.grid.text)
        r = int(self.screen.ids.rotation.text)

        on_grid_x = int(round(pos[0]/grid) * grid)
        on_grid_y = int(round(pos[1]/grid) * grid)

        draw_ent = self.gameworld.entities[self.asset_id]
        draw_ent.position.pos = (on_grid_x, on_grid_y)
        draw_ent.cymunk_physics.body.position = draw_ent.position.pos

        draw_ent.cymunk_physics.body.angle = radians(r)

    def delete_at(self, pos):
        FLUFF = 25
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

        # if touch.button == 'left':
        if self.deleting:
            self.delete_at(pos)

        else:
            if self.entity_to_place == '':
                return

            grid = int(self.screen.ids.grid.text)
            r = int(self.screen.ids.rotation.text)

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

        # elif touch.button == 'scrollup':
            # cam.camera_scale = cam.camera_scale + 0.1

        # elif touch.button == 'scrolldown':
            # cam.camera_scale = cam.camera_scale - 0.1

        # elif touch.button == 'middle':
            # cam.focus_entity = False
            # cam.do_scroll_lock = False
            # cam.look_at(pos)


Factory.register('LevelEditorSystem', cls=LevelEditorSystem)
