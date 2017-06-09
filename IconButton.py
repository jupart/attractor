from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image


class IconButton(ButtonBehavior, Image):

    def __init__(self, source, num, **kwargs):
        super(IconButton, self).__init__(**kwargs)
        self.source = source
        self.num = num
