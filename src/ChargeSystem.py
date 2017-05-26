from kivy.app import App
from kivent_core.systems.gamesystem import Component
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory


class ChargeComponent(Component):
    def __init__(self, **kwargs):
        pass

    def update_charge(self, ent, change_to):
        ent.charge.charge = change_to


class ChargeSystem(GameSystem):
    def __init__(self, **kwargs):
        super(ChargeSystem, self).__init__(**kwargs)

    def update(self, dt):
        entities = self.gameworld.entities
        attractor = entities[App.get_running_app().game.attractor_id]

        if attractor.charge.charge == 'n':
            return

        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = entities[entity_id]

                # Only dipoles exert force and only on the attractor
                if entity.charge == '+/-':
                    if self.in_range(entity.position.pos,
                                     entity.rotate,
                                     attractor.position.pos):
                        self.exert_force(entity.position.pos,
                                         entity.rotate,
                                         attractor.position.pos,
                                         attractor.charge.charge)

    def in_range(self, dipole_pos, dipole_rotate, attractor_pos):
        pass

    def exert_force(self, dipole_pos, dipole_rotate, attractor_pos, attractor_charge):
        pass


Factory.register('ChargeSystem', cls=ChargeSystem)
