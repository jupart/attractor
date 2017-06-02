import json
from math import radians


class EntityFactory():
    def __init__(self, gameworld_init_entity, **kwargs):
        self.gameworld_init_entity = gameworld_init_entity
        self.reload_entity_data()

    def reload_entity_data(self):
        with open('resources/entities.json') as j_file:
            data = json.load(j_file)
        self.entity_data = data['entities']

    def create_entity_at(self, name, x, y, rot=0):
        # Find a match for "name" within entity_data
        for ent in self.entity_data:
            if ent['name'] == name:
                new_ent_data = self.get_entity_data(ent)
                new_ent_data[0]['cymunk_physics']['position'] = (x, y)
                new_ent_data[0]['position'] = (x, y)
                if 'rotate' in new_ent_data[0]:
                    new_ent_data[0]['cymunk_physics']['angle'] = radians(rot)
                    new_ent_data[0]['rotate'] = radians(rot)
                    new_ent_data[0]['rotate_renderer']['rotate'] = radians(rot)
                return self.gameworld_init_entity(new_ent_data[0],
                                                  new_ent_data[1])
        else:
            return False

    def get_entity_data(self, entity):
        c_data = {}
        for comp in entity['components']:
            # dict.update() appends a dict to another dict
            c_data.update(self.get_component_data(comp))

        c_order = []
        if 'position' in c_data:
            c_order.append('position')
        if 'rotate' in c_data:
            c_order.append('rotate')
        if 'rotate_renderer' in c_data:
            c_order.append('rotate_renderer')
        if 'animation' in c_data:
            c_order.append('animation')
        if 'charge' in c_data:
            c_order.append('charge')
        if 'cymunk_physics' in c_data:
            c_order.append('cymunk_physics')

        return [c_data, c_order]

    def get_component_data(self, component_data):
        if component_data['type'] == 'render':
            c_dict = {'rotate_renderer': {'texture': component_data['texture'],
                                          'size': (component_data['size_x'],
                                                   component_data['size_y']),
                                          'model_key': component_data['texture'],
                                          'render': True}}

        elif component_data['type'] == 'rotate':
            c_dict = {'rotate': component_data['rotation']}

        elif component_data['type'] == 'velocity':
            c_dict = {'velocity': {'x': component_data['x'],
                                   'y': component_data['y']}}

        elif component_data['type'] == 'position':
            c_dict = {'position': {'x': component_data['x'],
                                   'y': component_data['y']}}

        elif component_data['type'] == 'charge':
            c_dict = {'charge': {'charge': component_data['charge'],
                                 'strength': component_data['strength']}}

        elif component_data['type'] == 'animation':
            c_dict = {'animation': {'name': component_data['animation'],
                                    'loop': component_data['looped']}}

        elif component_data['type'] == 'physics':
            col_shapes = []
            for circle in component_data['circles']:
                col_shapes.append({'shape_type': 'circle',
                                   'elasticity': 0,
                                   'collision_type': 1,
                                   'shape_info': {'inner_radius': 0,
                                                  'outer_radius': circle['radius'],
                                                  'mass': component_data['mass'],
                                                  'offset': (circle['offset_x'],
                                                             circle['offset_y'])},
                                   'friction': 1.0})
            for seg in component_data['segments']:
                col_shapes.append({'shape_type': 'segment',
                                   'elasticity': 0,
                                   'collision_type': 1,
                                   'shape_info': {'a': (seg['ax'], seg['ay']),
                                                  'b': (seg['bx'], seg['by']),
                                                  'mass': component_data['mass'],
                                                  'radius': seg['radius']},
                                   'friction': 1.0})

            c_dict = {'cymunk_physics': {'main_shape': component_data['shape'],
                                         'velocity': (0, 0),
                                         'position': (0, 0),
                                         'angle': 0,
                                         'angular_velocity': 0,
                                         'vel_limit': 1000,
                                         'ang_vel_limit': radians(200),
                                         'mass': component_data['mass'],
                                         'moment': component_data['moment'],
                                         'col_shapes': col_shapes}}

        else:
            return {}

        return c_dict

    def get_entity_names(self):
        names = []
        for ent in self.entity_data:
            names.append(ent['name'])

        return names


