from kivy.app import App
from kivy.animation import Animation
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory


class AlternatingPoleSystem(GameSystem):
    def __init__(self, **kwargs):
        super(AlternatingPoleSystem, self).__init__(**kwargs)

    def update(self, dt):
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = self.gameworld.entities[entity_id]

                time = entity.alternating_pole.time
                timeout = entity.alternating_pole.timeout

                if time > timeout:
                    time = 0
                    self.change_charge(entity)
                else:
                    time = time + dt

    def change_charge(self, ent):
        charge = ent.charge.charge
        pole1 = ent.alternating_pole.pole1
        pole2 = ent.alternating_pole.pole2

        if charge == pole1:
            charge = pole2
        else:
            charge = pole1


Factory.register('AlternatingPoleSystem', cls=AlternatingPoleSystem)
