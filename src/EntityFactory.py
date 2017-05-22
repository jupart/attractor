import os.path
import json


class EntityFactory():
    def __init__(self, gameworld_init_entity, **kwargs):
        self.gameworld_init_entity = gameworld_init_entity
        self.reload_entity_data()

    def reload_entity_data(self):
        json_file = 'resources/entities.json'
        with open('resources/entities.json') as j_file:
            data = json.load(j_file)
        self.entity_data = data['entities']

    def create_entity_at(self, name, x, y):
        # Find a match for "name" within entity_data
        for ent in self.entity_data:
            if ent['name'] == name:
                new_ent_data = self.get_entity_data(ent['name'])
                return self.gameworld_init_entity(new_ent_data[0],
                                                  new_ent_data[1])
        else:
            return False

    def get_entity_data(self, entity_data):
        c_data = {}
        for comp in entity_data['components']:
            # dict.update() appends a dict to another dict
            c_data.update(self.get_component_data(comp))

        c_order = []
        return [c_data, c_order]

    def get_component_data(self, component_data):
        if component_data['type'] == 'texture':
            c_dict = {'rotate_renderer': {'texture': component_data['texture'],
                                          'size': (component_data['size_x'],
                                                   component_data['size_y']),
                                          'model_key': component_data['texture'],
                                          'render': True}}

        elif component_data['type'] == 'movement':
            c_dict = {'movement': True}

        elif component_data['type'] == 'velocity':
            c_dict = {'velocity': {'x': component_data['x'],
                                   'y': component_data['y']}}

        elif component_data['type'] == 'position':
            c_dict = {'velocity': {'x': component_data['x'],
                                   'y': component_data['y']}}

        elif component_data['type'] == 'charge':
            c_dict = {'charge': component_data['charge']}

        elif component_data['type'] == 'animation':
            pass

        elif component_data['type'] == 'physics':
            pass

        else:
            return {}

        return c_dict
