#!python3

from kivy.app import App
from kivy.config import Config

import Game


class AttractorApp(App):
    def build(self):
        Config.set('kivy', 'exit_on_escape', '0')
        Config.set('graphics', 'width', '600')
        Config.set('graphics', 'height', '400')
        self.game = Game.AttractorGame()
        return self.game
