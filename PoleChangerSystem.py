from kivy.app import App
from kivy.graphics import Color, Ellipse
from kivy.animation import Animation
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory


class PoleChangerSystem(GameSystem):
    def __init__(self, **kwargs):
        super(PoleChangerSystem, self).__init__(**kwargs)

    def update(self, dt):
        attractor_id = App.get_running_app().game.attractor_id
        attractor = self.gameworld.entities[attractor_id]

        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = self.gameworld.entities[entity_id]

                pos = entity.position
                size = entity.pole_changer.size
                to_charge = entity.pole_changer.to
                attractor_pos = attractor.position

                if entity.pole_changer.rect is None:
                    if to_charge == '+':
                        r, g, b = 0.894, 0.243, 0.282
                    elif to_charge == '-':
                        r, g, b = 0.118, 0.490, 0.694
                    else:
                        r, g, b = 0.33, 0.33, 0.33

                    with App.get_running_app().game.ids.play_camera.canvas.before:
                        color = Color(r, g, b, -0.05)
                        entity.pole_changer.rect = Ellipse(size=(size[0],
                                                                 size[1]),
                                                           pos=(pos.x - size[0]/2,
                                                                pos.y - size[1]/2))

                    anim = Animation(a=0.1) + Animation(a=-0.05, duration=1)
                    anim.repeat = True
                    anim.start(color)

                if self.in_range(pos, size, attractor_pos):
                    if to_charge == '+':
                        new_anim = 'attractor_positive_idle'
                    elif to_charge == '-':
                        new_anim = 'attractor_negative_idle'
                    else:
                        new_anim = 'attractor_neutral_idle'

                    attractor.animation.animation = new_anim
                    attractor.charge.charge = to_charge

    def in_range(self, pos, size, attractor_pos):
        left = pos.x - size[0]/2
        right = pos.x + size[0]/2
        top = pos.y + size[1]/2
        bottom = pos.y - size[1]/2

        x = attractor_pos.x
        y = attractor_pos.y

        if (left < x) and (x < right) and (bottom < y) and (y < top):
            return True
        else:
            return False

    def clear_component(self, component_index):
        entity_id = self.components[component_index].entity_id
        entity = self.gameworld.entities[entity_id]

        insruction = entity.pole_changer.rect
        if insruction is None:
            return

        canvas = App.get_running_app().game.ids.play_camera.canvas
        canvas.before.remove(insruction)


Factory.register('PoleChangerSystem', cls=PoleChangerSystem)
