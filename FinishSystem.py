from kivy.app import App
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory


class FinishSystem(GameSystem):
    def __init__(self, **kwargs):
        super(FinishSystem, self).__init__(**kwargs)

    def update(self, dt):
        attractor_id = App.get_running_app().game.attractor_id
        attractor = self.gameworld.entities[attractor_id]

        for component in self.components:
            if component is not None:
                attractor_pos = attractor.position.pos
                entity_id = component.entity_id
                finish = self.gameworld.entities[entity_id]

                if self.pos_is_in_finish(attractor_pos, finish):
                    App.get_running_app().game.finish_level()

    def pos_is_in_finish(self, pos, finish):
        left = finish.position.x - finish.finish.size[0]/2
        right = finish.position.x + finish.finish.size[0]/2
        top = finish.position.y + finish.finish.size[1]/2
        bottom = finish.position.y - finish.finish.size[1]/2

        x = pos[0]
        y = pos[1]

        if (left < x) and (x < right) and (bottom < y) and (y < top):
            return True
        else:
            return False


Factory.register('FinishSystem', cls=FinishSystem)
