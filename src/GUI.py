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
from datetime import datetime

kivy.require('1.11.0')

# evtl nachher True oder 'auto'
Window.fullscreen = False


class MyScreen(ScreenManager):

    def get_by_id(self, p_id) -> Widget:
        return self.ids.get(p_id)

    def add_entry(self):
        myBox = self.get_by_id('bl')
        myEntry = BoxLayout(orientation='horizontal', padding=20, spacing=10)
        # add Image
        img = Image()
        img.id = 'img'
        img.source = 'sbahn_Transparent.png'
        img.size = img.texture_size
        myEntry.add_widget(img)
        # add Label
        lbl = Label()
        lbl.id = 'lbl'
        lbl.markup = True
        lbl.text = '[size=60][color=55bb33]SBahn {}[/color][/size]'.format(datetime.now())
        myEntry.add_widget(lbl)

        # myEntry = MyEntry()
        myBox.add_widget(myEntry, 2)
        pass


class MvgWidgetApp(App):
    time = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        return MyScreen()

    def _update_clock(self, dt):
        self.time = time()
