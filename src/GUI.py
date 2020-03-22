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

import Model

kivy.require('1.11.0')

# evtl nachher True oder 'auto'
Window.fullscreen = False


class MyEntry:
    label = None
    img_path = None
    destination = None
    from_ = None
    to_ = None
    connection_type = None
    departure = None
    arrival = None


class MyScreen(ScreenManager):

    def get_by_id(self, p_id) -> Widget:
        return self.ids.get(p_id)

    def add_entry(self, my_entry: MyEntry):
        _my_box = self.get_by_id('bl')
        new_entry = BoxLayout(orientation='horizontal', padding=20, spacing=10)
        # add Image
        img = Image()
        img.id = 'img'
        img.source = my_entry.img_path
        img.size = img.texture_size
        new_entry.add_widget(img)
        # add Label
        _lbl = Label()
        _lbl.id = '_lbl'
        _lbl.markup = True
        _lbl.text = '[size=40][color=55bb33]SBahn {}[/color][/size]'.format(my_entry.departure)
        new_entry.add_widget(_lbl)

        _my_box.add_widget(new_entry, 2)
        pass

    def add_route(self, route: str):
        _my_box = self.get_by_id('vxv')
        _lbl = Label()
        _lbl.id = 'lbl'
        _lbl.markup = True
        _lbl.text = '[size=30][color=44eeee]{}[/color][/size]'.format(route)
        _lbl.size_hint = (1, 0.000001)
        _my_box.add_widget(_lbl, 4)


class MvgWidgetApp(App):
    time = NumericProperty(0)
    screen: MyScreen = None

    def build(self):
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screen = MyScreen()
        self.screen.add_route(Model.get_route())
        _departures = Model.get_next_departures()
        for el in _departures:
            print(el)
            self.screen.add_entry(el)

        return self.screen

    def _update_clock(self, dt):
        self.time = time()
