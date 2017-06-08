from kivy.app import App
from kivy.graphics import Color, Ellipse
from kivy.animation import Animation
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory


class ChargeSystem(GameSystem):
    DISTANCE_MOD = 400
    FORCE_MOD = 3000

    def __init__(self, **kwargs):
        super(ChargeSystem, self).__init__(**kwargs)

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
                    screen_pos = entity.position.pos
                    radius = self.DISTANCE_MOD * abs(entity.charge.strength)

                    if entity.charge.charge == '+':
                        r, g, b = 0xe4, 0x3e, 0x48
                    elif entity.charge.charge == '-':
                        r, g, b = 0x1e, 0x7d, 0xb1

                    with App.get_running_app().game.canvas:
                        color = Color(r, g, b, 0.06)
                        entity.charge.ellipse = Ellipse(size=(radius * 2 + 40, radius * 2),
                                                        pos=screen_pos)

                    anim = Animation(a=0.5) + Animation(a=0.06, duration=1.)
                    anim.repeat = True
                    anim.start(color)
                    entity.charge.drawn = True

                else:
                    cam = App.get_running_app().game.ids.play_camera
                    cam_pos = cam.camera_pos
                    cam_scale = cam.camera_scale

                    screen_pos = ((entity.position.pos[0] + cam_pos[0]) / cam_scale,
                                  (entity.position.pos[1] + cam_pos[1]) / cam_scale)
                    entity.charge.ellipse.pos = screen_pos

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

    def exert_force(self, pos, strength, attractor):
        offset = (attractor.position.x - pos.x, attractor.position.y - pos.y)

        if attractor.charge.charge == '+':
            mod = 1
        else:
            mod = -1

        d = ((pos.x - attractor.position.x)**2 + (pos.y - attractor.position.y)**2)
        f = mod * (strength * self.FORCE_MOD)/d
        force = (offset[0] * f, offset[1] * f)

        attractor.cymunk_physics.body.apply_impulse(force, offset)


Factory.register('ChargeSystem', cls=ChargeSystem)
