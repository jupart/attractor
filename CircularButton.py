from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.vector import Vector

class CircularButton(ButtonBehavior, Widget):
    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2
