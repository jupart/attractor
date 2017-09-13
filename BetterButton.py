from kivy.uix.button import Button


class BetterButton(Button):
    def __init__(self, *args, **kwargs):
        super(BetterButton, self).__init__(*args, **kwargs)
        self.grabbed = False

    def on_touch_down(self, touch):
        super(BetterButton, self).on_touch_down(touch)
        if self.collide_point(touch.x, touch.y):
            if self.grabbed == False:
                self.dispatch('on_press')
                touch.grab(self)
                self.grabbed = True
                return True
            else:
                return True

    def on_touch_up(self, touch):
        super(BetterButton, self).on_touch_up(touch)
        if touch.grab_current is self:
            self.dispatch('on_release')
            touch.ungrab(self)
            self.grabbed = False
            return True
