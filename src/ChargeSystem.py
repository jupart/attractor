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
        attractor_id = App.get_running_app().game.attractor_id
        attractor = entities[attractor_id]

        if attractor.charge.charge == 'n':
            return

        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                if entity_id == attractor_id:
                    continue

                entity = entities[entity_id]

                if entity.charge != 'n':
                    if self.in_range(entity.position.pos,
                                     entity.charge.strength,
                                     attractor.position.pos):
                        self.exert_force(entity.position.pos,
                                         entity.charge.strength,
                                         attractor.position.pos,
                                         attractor.charge.charge)

    def in_range(self, pos, strength, attractor_pos):
        # some arbitrary radius based on strength arg
        # first check > or < pos +/- radius, then
            # (x - center_x)^2 + (y - center_y)^2 < radius^2
        pass

    def exert_force(self, pos, strength, attractor_pos, attractor_charge):
        # sqrt((pos.x - attractor_pos.x)^2 + (pos.y - attractor_pos.y)^2) * strength * some_mod
        pass


Factory.register('ChargeSystem', cls=ChargeSystem)
