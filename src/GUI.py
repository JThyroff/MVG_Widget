from time import time

import kivy
from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.settings import SettingsWithNoMenu
from kivy.uix.widget import Widget

import Model

kivy.require('1.11.0')
# evtl nachher True oder 'auto'
Window.fullscreen = False

routeStr: str = '[color=44eeee]{}[/color]'
color_text: str = '[color=cccccc]'
color_h_text: str = '[color=eeffaa]'
color_close: str = '[/color]'
font_size = 20


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
        lbl_lbl = Label()
        lbl_lbl.id = 'lbl_lbl'
        lbl_lbl.size_hint_x = 0.5
        lbl_lbl.size_hint_y = 1
        lbl_lbl.markup = True
        lbl_lbl.text = (color_text + '{} {}' + color_close).format(my_entry.label, my_entry.destination)
        lbl_lbl.font_size = font_size
        lbl_lbl.halign = 'left'
        lbl_lbl.valign = 'middle'
        # lbl_lbl.texture_size = new_entry.size
        # lbl_lbl.text_size = new_entry.size
        lbl_lbl.pos_hint = {'center_x': .3, 'center_y': .5}
        new_entry.add_widget(lbl_lbl)

        # add time Label
        time_lbl = Label()
        time_lbl.id = 'time_lbl'
        time_lbl.size_hint_x = 0.3
        time_lbl.markup = True
        time_lbl.text = (color_h_text + '{}' + color_close + ' >> ').format(
            my_entry.departure) + (color_h_text + '{}' + color_close).format(
            my_entry.arrival)
        time_lbl.font_size = font_size
        time_lbl.pos_hint = {'right': 1, 'center_y': .5}
        new_entry.add_widget(time_lbl)

        _my_box.add_widget(new_entry, 0)
        pass

    def set_route(self, route: str):
        _lbl: Label = self.get_by_id('route_lbl')
        _lbl.font_size = font_size
        _lbl.text = routeStr.format(route)


class MvgWidgetApp(App):
    time = NumericProperty(0)
    screen: MyScreen = None

    def build(self):
        Window.size = (480, 320)
        self.settings_cls = MySettingsWithPanel
        # settings and config
        # root = Builder.load_string(kv)
        # label = root.ids.label
        Model.start_str = self.config.get('MVG Widget', 'start')
        Model.destination_str = self.config.get('MVG Widget', 'dest')
        Model.amount = int(self.config.get('MVG Widget', 'amount'))
        global font_size
        font_size = float(self.config.get('MVG Widget', 'font_size'))
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
        config.setdefaults('MVG Widget', {'start': 'Dachau', 'dest': 'Forschungszentrum', 'amount': 3, 'font_size': 20})

    def build_settings(self, settings):
        settings.add_json_panel('MVG Widget', self.config, 'settings.json')

    def on_config_change(self, config, section, key, value):
        Logger.info("App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "MVG Widget":
            if key == "start":
                Model.start_str = value
            elif key == "dest":
                Model.destination_str = value
            elif key == "amount":
                Model.amount = int(value)
            elif key == 'font_size':
                global font_size
                font_size = float(self.config.get('MVG Widget', 'font_size'))

    def close_settings(self, settings=None):
        Logger.info("App.close_settings: {0}".format(settings))
        super(MvgWidgetApp, self).close_settings(settings)
        self._update(-1)

    def _update(self, dt):
        Logger.info('[Widget.update] updating data and view')
        self.time = time()
        # route update
        self.screen.set_route(Model.get_route())
        # connection update
        self.screen.get_by_id('bl').clear_widgets()
        _departures = Model.get_next_departures()
        for el in _departures:
            self.screen.add_entry(el)


class MySettingsWithPanel(SettingsWithNoMenu):
    """
    It is not usually necessary to create subclass of a settings panel. There
    are many built-in types that you can use out of the box
    (SettingsWithSidebar, SettingsWithSpinner etc.).

    You would only want to create a Settings subclass like this if you want to
    change the behavior or appearance of an existing Settings class.
    """

    def build(self):
        self.add_widget(Button())

    def on_close(self):
        Logger.info("MySettingsWithPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
            "MySettingsWithPanel.on_config_change: "
            "{0}, {1}, {2}, {3}".format(config, section, key, value))
