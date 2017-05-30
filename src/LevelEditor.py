from kivy.app import App
from kivy.core.window import Window
from kivent_core.systems.gamesystem import Component
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory
from kivy.clock import Clock


class LevelEditorComponent(Component):

    def __init__(self, **kwargs):
        super(LevelEditorComponent, self).__init__(**kwargs)
        self.asset = ''
        self.previous_asset = 'None'
        self.draw_id = -1
        self.draw_renderer = 'renderer'


class LevelEditorSystem(GameSystem):

    def __init__(self, **kwargs):
        super(LevelEditorSystem, self).__init__(**kwargs)
        self.enabled = False

    def update(self, dt):
        entities = self.gameworld.entities
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = entities[entity_id]

                if not self.enabled:
                    if entity.level_editor.draw_id != -1:
                        self.gameworld.remove_entity(entity.level_editor.draw_id)
                        entity.level_editor.draw_id = -1
                        entity.level_editor.asset = ''

                else:
                    try:
                        asset = entity.level_editor.asset
                    except AttributeError:
                        continue

                    if entity.level_editor.previous_asset != asset:
                        entity.level_editor.previous_asset = asset
                        if asset == '':
                            asset = entity.level_editor.asset = 'bullet0'
                            entity.level_editor.previous_asset = asset

                        if '_r' in asset:
                            tex_name = asset[:-2]
                        else:
                            tex_name = asset

                        if entity.level_editor.draw_id != -1:
                            self.gameworld.remove_entity(entity.level_editor.draw_id)

                        component_dict = {'position': (0, 0),
                                          'renderer': {'texture': tex_name,
                                                       'size': (100, 100),
                                                       'model_key': asset,
                                                       'render': True}}

                        component_order = ['position', 'renderer']

                        ent_id = self.gameworld.init_entity(component_dict,
                                                            component_order)
                        entity.level_editor.draw_id = ent_id

                    app = App.get_running_app()
                    cam_pos = app.game.ids.camera.camera_pos
                    scale = app.game.ids.camera.camera_scale
                    pos = (Window.mouse_pos[0] * scale - cam_pos[0],
                           Window.mouse_pos[1] * scale - cam_pos[1])

                    try:
                        grid = int(app.game.grid.text)
                    except ValueError:
                        grid = 1

                    on_grid_x = int(round(pos[0]/grid) * grid)
                    on_grid_y = int(round(pos[1]/grid) * grid)

                    draw_ent = self.gameworld.entities[entity.level_editor.draw_id]
                    draw_ent.position.pos = (on_grid_x, on_grid_y)


Factory.register('LevelEditorSystem', cls=LevelEditorSystem)
