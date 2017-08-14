import json
from math import radians

from cymunk import PinJoint


class EntityFactory():
    ROTATE_MOD = 1000

    def __init__(self, gameworld, physics, **kwargs):
        self.gameworld = gameworld
        self.physics = physics
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

                if 'cymunk_physics' in new_ent_data[0]:
                    new_ent_data[0]['cymunk_physics']['position'] = (x, y)

                new_ent_data[0]['position'] = (x, y)

                if 'rotate' in new_ent_data[0]:
                    new_ent_data[0]['rotate'] = radians(rot)

                    if 'rotate_renderer' in new_ent_data[0]:
                        new_ent_data[0]['rotate_renderer']['rotate'] = radians(rot)

                    if 'cymunk_physics' in new_ent_data[0]:
                        new_ent_data[0]['cymunk_physics']['angle'] = radians(rot)

                if 'attach' in new_ent_data[0]:
                    attach = new_ent_data[0].pop('attach')
                    ids = self.gameworld.init_entity(new_ent_data[0], new_ent_data[1])
                    ids2 = self.create_entity_at(attach['entity'],
                                                 x,
                                                 y + attach['distance'])

                    rotator = self.gameworld.entities[ids]
                    rotated = self.gameworld.entities[ids2]

                    # Get started rotating
                    direction = -1 if attach['direction'] == 'cw' else 1

                    body = rotated.cymunk_physics.body
                    force = new_ent_data[0]['cymunk_physics']['angular_velocity']
                    body.apply_impulse((direction * self.ROTATE_MOD * force, 0), (-10, 0))

                    constraint = PinJoint(rotator.cymunk_physics.body,
                                          rotated.cymunk_physics.body,
                                          (0, 0),
                                          (0, 0))
                    self.physics.space.add_constraint(constraint)
                    return ids

                if 'membrane' in new_ent_data[0]:
                    membrane = new_ent_data[0].pop('membrane')

                    # Change their collision group to 2
                    shapes = new_ent_data[0]['cymunk_physics']['col_shapes']
                    for shape in shapes:
                        shape['collision_type'] = 2


                return self.gameworld.init_entity(new_ent_data[0], new_ent_data[1])
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
        # if 'mid_renderer' in c_data:
            # c_order.append('mid_renderer')
        # if 'bg_renderer' in c_data:
            # c_order.append('bg_renderer')
        if 'animation' in c_data:
            c_order.append('animation')
        if 'charge' in c_data:
            c_order.append('charge')
        if 'cymunk_physics' in c_data:
            c_order.append('cymunk_physics')
        if 'pole_changer' in c_data:
            c_order.append('pole_changer')
        if 'finish' in c_data:
            c_order.append('finish')

        return [c_data, c_order]

    # TODO could be a lookup instead of if branches
    def get_component_data(self, component_data):
        if component_data['type'] == 'render':
            c_dict = {'rotate_renderer': {'texture': component_data['texture'],
                                          'size': (component_data['size_x'],
                                                   component_data['size_y']),
                                          'model_key': component_data['texture'].encode('utf-8'),
                                          'render': True}}

        # if component_data['type'] == 'bg_render':
            # c_dict = {'bg_renderer': {'texture': component_data['texture'],
                                      # 'size': (component_data['size_x'],
                                               # component_data['size_y']),
                                      # 'model_key': component_data['texture'].encode('utf-8'),
                                      # 'render': True}}

        elif component_data['type'] == 'rotate':
            c_dict = {'rotate': component_data['rotation']}

        elif component_data['type'] == 'velocity':
            c_dict = {'velocity': {'x': component_data['x'],
                                   'y': component_data['y']}}

        elif component_data['type'] == 'position':
            c_dict = {'position': (component_data['x'],
                                   component_data['y'])}

        elif component_data['type'] == 'charge':
            c_dict = {'charge': {'charge': component_data['charge'].encode('utf-8'),
                                 'skip': False,
                                 'strength': component_data['strength'],
                                 'drawn': False,
                                 'ellipse': None}}

        elif component_data['type'] == 'animation':
            c_dict = {'animation': {'name': component_data['animation'],
                                    'loop': component_data['looped']}}

        elif component_data['type'] == 'physics':
            col_shapes = []
            for circle in component_data['circles']:
                col_shapes.append({'shape_type': 'circle',
                                   'elasticity': 0.6,
                                   'collision_type': 1,
                                   'shape_info': {'inner_radius': 0,
                                                  'outer_radius': circle['radius'],
                                                  'mass': component_data['mass'],
                                                  'offset': (circle['offset_x'],
                                                             circle['offset_y'])},
                                   'friction': 1.0})
            for seg in component_data['segments']:
                col_shapes.append({'shape_type': 'segment',
                                   'elasticity': 0.6,
                                   'collision_type': 1,
                                   'shape_info': {'a': (seg['ax'], seg['ay']),
                                                  'b': (seg['bx'], seg['by']),
                                                  'mass': component_data['mass'],
                                                  'radius': seg['radius']},
                                   'friction': 1.0})

            if 'angular_velocity' in component_data:
                ang_vel = component_data['angular_velocity']
            else:
                ang_vel = 0

            if component_data['moment'] == 'inf':
                mom = float('inf')
            else:
                mom = component_data['moment']

            c_dict = {'cymunk_physics': {'main_shape': component_data['shape'],
                                         'velocity': (0, 0),
                                         'position': (0, 0),
                                         'angle': 0,
                                         'angular_velocity': ang_vel,
                                         'vel_limit': 1000,
                                         'ang_vel_limit': radians(45),
                                         'mass': component_data['mass'],
                                         'moment': mom,
                                         'col_shapes': col_shapes}}

        elif component_data['type'] == 'attach':
            c_dict = {'attach': {'entity': component_data['entity'],
                                 'distance': component_data['distance'],
                                 'direction': component_data['direction']}}

        elif component_data['type'] == 'finish':
            c_dict = {'finish': {'size': (component_data['size_x'],
                                          component_data['size_y'])}}

        elif component_data['type'] == 'pole_changer':
            c_dict = {'pole_changer': {'size': (component_data['size_x'],
                                                component_data['size_y']),
                                       'to': component_data['to'],
                                       'rect': None}}

        elif component_data['type'] == 'membrane':
            c_dict = {'charge': {'charge': component_data['pole'].encode('utf-8'),
                                 'skip': True,
                                 'strength': 1,
                                 'drawn': False,
                                 'ellipse': None}}
            membrane_dict = {'membrane': None}
            c_dict.update(membrane_dict)

        else:
            return {}

        return c_dict

    def get_entity_names(self):
        names = []
        for ent in self.entity_data:
            names.append(ent['name'])

        return names
