import kivy

from time import time

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty

kivy.require('1.11.0')

# evtl nachher True oder 'auto'
Window.fullscreen = False


class MvgWidgetApp(App):
    time = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self._update_clock, 1 / 60.)

    def _update_clock(self, dt):
        self.time = time()

    def add_entry(self):

        pass
