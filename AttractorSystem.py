from kivy.app import App
from kivy.graphics import Color, Ellipse, PushMatrix, PopMatrix, Rotate
from kivy.animation import Animation
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory

from cymunk import Vec2d

from math import degrees


class AttractorSystem(GameSystem):
    DAMPING = 0.7

    def __init__(self, **kwargs):
        super(AttractorSystem, self).__init__(**kwargs)

    def update(self, dt):
        attractor_id = App.get_running_app().game.attractor_id
        attractor = self.gameworld.entities[attractor_id]

        # Apply damping
        vx, vy = attractor.cymunk_physics.body.velocity
        if (vx, vy) != (0, 0):
            vx = vx - (vx * self.DAMPING * dt)
            vy = vy - (vy * self.DAMPING * dt)
            attractor.cymunk_physics.body.velocity = (vx, vy)

        ry = attractor.cymunk_physics.body.angular_velocity
        if ry != 0:
            ry = ry - (ry * self.DAMPING * dt)
            attractor.cymunk_physics.body.angular_velocity = ry

        r = 30 * 2
        x, y = attractor.position.pos[0], attractor.position.pos[1]
        s = 5

        # Draw shapes if needed
        if not attractor.attractor.drawn:
            with App.get_running_app().game.ids.play_camera.canvas.before:
                PushMatrix()
                attractor.attractor.rotate = Rotate(angle=0, axis=(0, 0, 1),
                                                    origin=(x, y))

            with App.get_running_app().game.ids.play_camera.canvas.after:
                # Outlines
                outline_color = Color(0.196, 0.302, 0.376, 1)
                outline1 = Ellipse(size=(r, r), pos=(x - r, y - r))
                outline2 = Ellipse(size=(r, r), pos=(x - r, y - r))

                # Fill
                fill_color = Color(0.314, 0.376, 0.412, 1)
                fill1 = Ellipse(size=(r - s, r - s), pos=(x - r - s, y - r - s))
                fill2 = Ellipse(size=(r - s, r - s), pos=(x - r - s, y - r - s))

                attractor.attractor.shapes = [outline1, fill1, outline2, fill2]
                attractor.attractor.outline = outline_color
                attractor.attractor.fill = fill_color
                attractor.attractor.drawn = True

                PopMatrix()

        # Update rotation and rotation origin
        attractor.attractor.rotate.origin = (x, y)
        attractor.attractor.rotate.angle = degrees(attractor.cymunk_physics.body.angle)

        # Update it's position and rotation
        for shape in attractor.attractor.shapes:
            shape.pos = (x - shape.size[0]/2, y - shape.size[1]/2)

        # Change if needed
        if attractor.attractor.to_change:
            time = 0.9
            line = 'out_expo'
            pole = attractor.attractor.to_change

            red_outline = [0.6, 0.082, 0.106, 1]
            blue_outline = [0.094, 0.388, 0.557, 1]
            grey_outline = [0.196, 0.302, 0.376, 1]

            red_fill = [0.894, 0.306, 0.282, 1]
            blue_fill = [0.118, 0.490, 0.694, 1]
            grey_fill = [0.314, 0.376, 0.412, 1]

            if pole == '+':
                fill_anim = Animation(r=red_fill[0], g=red_fill[1], b=red_fill[2],
                                      d=time, t=line)
                outline_anim = Animation(r=red_outline[0], g=red_outline[1], b=red_outline[2],
                                         d=time, t=line)
                size_anim1 = Animation(size=(r * 0.5, r), d=time, t=line)
                size_anim2 = Animation(size=(r * 0.5 - s, r - s), d=time, t=line)
                size_anim3 = Animation(size=(r, r * 0.5), d=time, t=line)
                size_anim4 = Animation(size=(r - s, r * 0.5 - s), d=time, t=line)
            elif pole == '-':
                fill_anim = Animation(r=blue_fill[0], g=blue_fill[1], b=blue_fill[2],
                                      d=time, t=line)
                outline_anim = Animation(r=blue_outline[0], g=blue_outline[1], b=blue_outline[2],
                                         d=time, t=line)
                size_anim1 = Animation(size=(r * 0.7, r * 0.7), d=time, t=line)
                size_anim2 = Animation(size=(r * 0.7 - s, r * 0.7 - s), d=time, t=line)
                size_anim3 = Animation(size=(r, r * 0.5), d=time, t=line)
                size_anim4 = Animation(size=(r - s, r * 0.5 - s), d=time, t=line)
            elif pole == 'r':
                fill_anim = Animation(r=0.314, g=0.314, b=0.314, d=0.5, t=line)
                outline_anim = Animation(r=0.314, g=0.314, b=0.314, d=0.5, t=line)
                size_anim1 = Animation(size=(0, 0), d=0.5, t=line)
                size_anim2 = Animation(size=(0, 0), d=0.5, t=line)
                size_anim3 = Animation(size=(0, 0), d=0.5, t=line)
                size_anim4 = Animation(size=(0, 0), d=0.5, t=line)
            elif pole == 'f':
                fill_anim = Animation(r=0, g=0, b=0, d=0.6, t='in_expo')
                outline_anim = Animation(r=0, g=0, b=0, d=0.6, t='in_expo')
                size_anim1 = Animation(size=(0, 0), d=0.6, t='in_expo')
                size_anim2 = Animation(size=(0, 0), d=0.6, t='in_expo')
                size_anim3 = Animation(size=(0, 0), d=0.6, t='in_expo')
                size_anim4 = Animation(size=(0, 0), d=0.6, t='in_expo')
            else:
                fill_anim = Animation(r=grey_fill[0], g=grey_fill[1], b=grey_fill[2],
                                      d=time, t=line)
                outline_anim = Animation(r=grey_outline[0], g=grey_outline[1], b=grey_outline[2],
                                         d=time, t=line)
                size_anim1 = Animation(size=(r, r), d=time, t=line)
                size_anim2 = Animation(size=(r - s, r - s), d=time, t=line)
                size_anim3 = Animation(size=(r, r), d=time, t=line)
                size_anim4 = Animation(size=(r - s, r - s), d=time, t=line)

            attractor.attractor.to_change = False

            fill_anim.start(attractor.attractor.fill)
            outline_anim.start(attractor.attractor.outline)
            size_anim1.start(attractor.attractor.shapes[0])
            size_anim2.start(attractor.attractor.shapes[1])
            size_anim3.start(attractor.attractor.shapes[2])
            size_anim4.start(attractor.attractor.shapes[3])


Factory.register('AttractorSystem', cls=AttractorSystem)
