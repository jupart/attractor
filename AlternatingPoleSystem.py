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
                timeout = entity.alternating_pole.speed

                if entity.alternating_pole.time > 
Factory.register('AlternatingPoleSystem', cls=AlternatingPoleSystem)
