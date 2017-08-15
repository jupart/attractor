#!/home/jpartain/Code/attractor/attractor/bin/python

import sys

from kivy.utils import platform

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

if platform == 'unix':
    import cProfile

import Game


class AttractorApp(App):
    def on_start(self):
        if platform == 'unix':
            self.profile = cProfile.Profile()
            self.profile.enable()

    def on_stop(self):
        if platform == 'unix':
            self.profile.disable()
            self.profile.dump_stats('app.profile')

    def build(self):
        Config.set('kivy', 'exit_on_escape', '0')
        Config.set('graphics', 'width', '300')
        Config.set('graphics', 'height', '200')
        Config.set('input', 'mouse', 'mouse,disable_multitouch')

        Window.set_title('Attractor')
        Window.clearcolor = (0.157, 0.157, 0.157, 1)

        self.game = Game.AttractorGame()
        return self.game


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    AttractorApp().run()
