from time import time

import kivy
from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.widget import Widget

import Model

kivy.require('1.11.0')
# evtl nachher True oder 'auto'
Window.fullscreen = False
routeStr: str = '[size=30][color=44eeee]{}[/color][/size]'


class MyEntry:
    label = None
    img_path = None
    destination = None
    from_ = None
    to_ = None
    connection_type = None
    departure: str = None
    arrival: str = None


class MyScreen(ScreenManager):

    def get_by_id(self, w_id) -> Widget:
        # print(self.ids)
        return self.ids.get(w_id)

    def add_entry(self, my_entry: MyEntry):
        _my_box = self.get_by_id('bl')
        # new_entry = BoxLayout(orientation='horizontal', padding=20, spacing=10)
        new_entry = FloatLayout()
        new_entry.size_hint = (1, 1)
        # add Image
        img = Image()
        img.id = 'img'
        img.size_hint_x = 0.13
        img.source = my_entry.img_path
        img.size = img.texture_size
        img.pos_hint = {'x': 0, 'center_y': .5}
        new_entry.add_widget(img)

        # add label Label
        _lbl_lbl = Label()
        _lbl_lbl.id = '_lbl_lbl'
        _lbl_lbl.size_hint_x = 0.3
        _lbl_lbl.markup = True
        _lbl_lbl.text = '[size=40][color=55bb33]{} {}[/color][/size]'.format(my_entry.label, my_entry.destination)
        _lbl_lbl.pos_hint = {'center_x': .3, 'center_y': .5}
        new_entry.add_widget(_lbl_lbl)

        # add time Label
        _time_lbl = Label()
        _time_lbl.id = '_time_lbl'
        _time_lbl.size_hint_x = 0.3
        _time_lbl.markup = True
        _time_lbl.text = '[size=60][color=55bb33]{} >> {}[/color][/size]'.format(my_entry.departure, my_entry.arrival)
        _time_lbl.pos_hint = {'right': 1, 'center_y': .5}
        new_entry.add_widget(_time_lbl)

        _my_box.add_widget(new_entry, 0)
        pass

    def set_route(self, route: str):
        _lbl: Label = self.get_by_id('routeLbl')
        _lbl.text = routeStr.format(route)


class MvgWidgetApp(App):
    time = NumericProperty(0)
    screen: MyScreen = None

    def build(self):
        self.settings_cls = MySettingsWithTabbedPanel
        # settings and config
        # root = Builder.load_string(kv)
        # label = root.ids.label
        self.config.get('My Label', 'text')
        float(self.config.get('My Label', 'font_size'))
        #
        self.screen = MyScreen()
        Clock.schedule_interval(self._update, 60)
        # set content
        self.screen.set_route(Model.get_route())
        _departures = Model.get_next_departures()
        for el in _departures:
            self.screen.add_entry(el)

        return self.screen

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('My Label', {'text': 'Hello', 'font_size': 20})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        settings.add_json_panel('My Label', self.config, 'settings.json')

    def _update(self, dt):
        print('updating data and view. ')
        self.time = time()
        # route update
        self.screen.set_route(Model.get_route())
        # connection update
        self.screen.get_by_id('bl').clear_widgets()
        _departures = Model.get_next_departures()
        for el in _departures:
            self.screen.add_entry(el)


class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    """
    It is not usually necessary to create subclass of a settings panel. There
    are many built-in types that you can use out of the box
    (SettingsWithSidebar, SettingsWithSpinner etc.).
    You would only want to create a Settings subclass like this if you want to
    change the behavior or appearance of an existing Settings class.
    """

    def on_close(self):
        Logger.info("main.py: MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
            "main.py: MySettingsWithTabbedPanel.on_config_change: "
            "{0}, {1}, {2}, {3}".format(config, section, key, value))
