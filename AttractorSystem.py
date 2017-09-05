from kivy.app import App
from kivy.graphics import Color, Ellipse, PushMatrix, PopMatrix, Rotate
from kivy.animation import Animation
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory

from cymunk import Vec2d


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

        r = 30
        x, y = attractor.position.pos[0], attractor.position.pos[1]

        # Draw shapes if needed
        if not attractor.attractor.drawn:
            with App.get_running_app().game.ids.play_camera.canvas.before:
                PushMatrix()
                attractor.attractor.rotate = Rotate()

                # Outlines
                outline_color = Color(0.196, 0.302, 0.376, 1)
                outline1 = Ellipse(size=(r, r), pos=(x - r, y - r))
                outline2 = Ellipse(size=(0, 0), pos=(x - r, y - r))

                # Fill
                fill_color = Color(0.314, 0.376, 0.412, 1)
                fill1 = Ellipse(size=(r - 3, r - 3), pos=(x - r - 3, y - r - 3))
                fill2 = Ellipse(size=(0, 0), pos=(x - r - 3, y - r - 3))

                attractor.attractor.shapes = [outline1, fill1, outline2, fill2]
                attractor.attractor.outline = outline_color
                attractor.attractor.fill = fill_color

            with App.get_running_app().game.ids.play_camera.canvas.after:
                PopMatrix()

        # Update it's position and rotation
        attractor.attractor.rotate = attractor.rotate
        for shape in attractor.attractor.shapes:
            shape.pos = (x - shape.size[0]/2, y - shape.size[1]/2)

        # Change if needed
        if attractor.attractor.to_change:
            time = 0.5
            line = 'out_circ'
            pole = attractor.attractor.to_change

            red_outline = [1, 1, 1, 1]
            blue_outline = [1, 1, 1, 1]
            grey_outline = [0.196, 0.302, 0.376, 1]

            red_fill = [1, 1, 1, 1]
            blue_fill = [1, 1, 1, 1]
            grey_fill = [0.314, 0.376, 0.412, 1]

            if pole == '+':
                fill_anim = Animation(fill=red_fill, d=time, t=line)
                outline_anim = Animation(fill=red_outline, d=time, t=line)
                size_anim1 = Animation(size=(r * 0.25, r), d=time, t=line)
                size_anim2 = Animation(size=(r * 0.25 - 3, r - 3), d=time, t=line)
                size_anim3 = Animation(size=(r, r * 0.25), d=time, t=line)
                size_anim4 = Animation(size=(r - 3, r * 0.25 - 3), d=time, t=line)
            elif pole == '-':
                fill_anim = Animation(fill=blue_fill, d=time, t=line)
                outline_anim = Animation(fill=blue_outline, d=time, t=line)
                size_anim1 = Animation(size=(r * 0.5, r * 0.5), d=time, t=line)
                size_anim2 = Animation(size=(r * 0.5 - 3, r * 0.5 - 3), d=time, t=line)
                size_anim3 = Animation(size=(r, r * 0.25), d=time, t=line)
                size_anim4 = Animation(size=(r - 3, r * 0.25 - 3), d=time, t=line)
            else:
                fill_anim = Animation(fill=grey_fill, d=time, t=line)
                outline_anim = Animation(fill=grey_outline, d=time, t=line)
                size_anim1 = Animation(size=(r, r), d=time, t=line)
                size_anim2 = Animation(size=(r - 3, r - 3), d=time, t=line)
                size_anim3 = Animation(size=(0, 0), d=time, t=line)
                size_anim4 = Animation(size=(0, 0), d=time, t=line)

            attractor.attractor.to_change = False

            fill_anim.start(attractor.attractor.fill)
            outline_anim.start(attractor.attractor.outline)
            size_anim1.start(attractor.attractor.shapes[0])
            size_anim2.start(attractor.attractor.shapes[1])
            size_anim3.start(attractor.attractor.shapes[2])
            size_anim4.start(attractor.attractor.shapes[3])


Factory.register('AttractorSystem', cls=AttractorSystem)
