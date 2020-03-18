import kivy

from time import time

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget

kivy.require('1.11.0')

# evtl nachher True oder 'auto'
Window.fullscreen = False


class MyEntry(BoxLayout):
    pass


class MyScreen(ScreenManager):

    def get_by_id(self, p_id)-> Widget:
        return self.ids.get(p_id)

    def add_entry(self):
        print('Test')
        myEntry = MyEntry()
        myBox = self.get_by_id('bl')
        print(myBox)
        print(myBox.name)
        myBox.add_widget(myEntry)
        pass


class MvgWidgetApp(App):
    time = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        return MyScreen()

    def _update_clock(self, dt):
        self.time = time()
