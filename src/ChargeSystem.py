from pubsub import pub

from kivent_core.systems.gamesystem import Component
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory


class ChargeComponent(Component):
    def __init__(self, **kwargs):
        self.charge = ''
        print('initcomponent')
        pub.subscribe(self.update_charge, 'charge')
        super().__init__(**kwargs)

    def update_charge(self, ent, change_to):
        print(change_to)
        ent.charge.charge = change_to


class ChargeSystem(GameSystem):
    def __init__(self, **kwargs):
        super(ChargeSystem, self).__init__(**kwargs)
        self.enabled = False

    def update(self, dt):
        # entities = self.gameworld.entities
        for component in self.components:
            if component is not None:
                pass
                # entity_id = component.entity_id
                # entity = entities[entity_id]


Factory.register('ChargeSystem', cls=ChargeSystem)
