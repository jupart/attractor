#!python3

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

import Game


class AttractorApp(App):
    def build(self):
        Config.set('kivy', 'exit_on_escape', '0')
        Config.set('graphics', 'width', '300')
        Config.set('graphics', 'height', '200')

        Window.set_title('Attractor')
        Window.clearcolor = (255, 253, 216, 216)

        self.game = Game.AttractorGame()
        return self.game


if __name__ == "__main__":
    AttractorApp().run()
