from kivy.uix.textinput import TextInput


class TouchedTextBox(TextInput):

    def __init__(self, **kwargs):
        super(TouchedTextBox, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        super(TouchedTextBox, self).on_touch_down(touch)

        if self.collide_point(touch.pos[0], touch.pos[1]):
            return True
        else:
            return False
