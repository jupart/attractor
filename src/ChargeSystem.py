from kivy.app import App
from kivent_core.systems.gamesystem import Component
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory
from kivy.graphics import Line, Color


class ChargeComponent(Component):
    def __init__(self, **kwargs):
        pass

    def update_charge(self, ent, change_to):
        ent.charge.charge = change_to


class ChargeSystem(GameSystem):
    CHARGE_MOD = 300

    def __init__(self, **kwargs):
        super(ChargeSystem, self).__init__(**kwargs)

    def update(self, dt):
        attractor_id = App.get_running_app().game.attractor_id
        attractor = self.gameworld.entities[attractor_id]

        if attractor.charge.charge != 'n':
            for component in self.components:
                if component is not None:
                    entity_id = component.entity_id
                    if entity_id == attractor_id:
                        continue

                    entity = self.gameworld.entities[entity_id]

                    if entity.charge.charge != 'n':
                        if self.in_range(entity.position,
                                         entity.charge.strength,
                                         attractor.position):
                            self.exert_force(entity.position,
                                             entity.charge.strength,
                                             attractor)

    def in_range(self, pos, strength, attractor_pos):
        radius = strength * self.CHARGE_MOD

        # Initial rectangle-based check
        if (attractor_pos.x < (pos.x - radius) or (pos.x + radius) < attractor_pos.x or
                attractor_pos.y < (pos.y - radius) or (pos.y + radius) < attractor_pos.y):
            return False

        if ((attractor_pos.x - pos.x)**2 + (attractor_pos.y - pos.y)**2) < radius**2:
            return True
        else:
            return False

    def exert_force(self, pos, strength, attractor):
        offset = (attractor.position.x - pos.x, attractor.position.y - pos.y)

        d = ((pos.x - attractor.position.x)**2 + (pos.y - attractor.position.y)**2)
        f = (strength * 10000)/d
        force = (offset[0] * f, offset[1] * f)

        attractor.cymunk_physics.body.apply_impulse(force, offset)


Factory.register('ChargeSystem', cls=ChargeSystem)
