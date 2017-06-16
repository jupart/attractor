from kivy.app import App
from kivy.graphics import Color, Rectangle
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
                if entity_id == attractor_id:
                    continue

                entity = self.gameworld.entities[entity_id]

                if not entity.charge.drawn:
                    radius = self.DISTANCE_MOD * abs(entity.charge.strength)

                    if entity.charge.charge == '+':
                        r, g, b = 0.894, 0.243, 0.282
                    elif entity.charge.charge == '-':
                        r, g, b = 0.118, 0.490, 0.694

                    with App.get_running_app().game.ids.play_camera.canvas:
                        color = Color(r, g, b, -0.05)
                        entity.charge.ellipse = Ellipse(size=(radius * 2,
                                                              radius * 2),
                                                        pos=(entity.position.x - radius,
                                                             entity.position.y - radius))

                    anim = Animation(a=0.1) + Animation(a=-0.05, duration=1)
                    anim.repeat = True
                    anim.start(color)
                    entity.charge.drawn = True

                else:
                    radius = self.DISTANCE_MOD * abs(entity.charge.strength)
                    entity.charge.ellipse.size = (radius * 2,
                                                  radius * 2)
                    entity.charge.ellipse.pos = (entity.position.x - radius,
                                                 entity.position.y - radius)

                if attractor.charge.charge != 'n':
                    if self.in_range(entity.position,
                                     entity.charge.strength,
                                     attractor.position):
                        self.exert_force(entity.position,
                                         entity.charge.strength,
                                         attractor)

    def in_range(self, pos, strength, attractor_pos):
        radius = abs(strength) * self.DISTANCE_MOD

        # Initial rectangle-based check
        if (attractor_pos.x < (pos.x - radius) or (pos.x + radius) < attractor_pos.x or
                attractor_pos.y < (pos.y - radius) or (pos.y + radius) < attractor_pos.y):
            return False

        if ((attractor_pos.x - pos.x)**2 + (attractor_pos.y - pos.y)**2) < radius**2:
            return True
        else:
            return False


Factory.register('PoleChangerSystem', cls=PoleChangerSystem)
