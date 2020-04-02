from time import time

import kivy
from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.settings import SettingsWithNoMenu
from kivy.uix.widget import Widget

import Model

"""
This file contains everything needed for the userinterface.
Objects of the class MyEntry are passed by the backend model to the frontend.
MyScreen derives from SreenManager and provides the root widget for MvgWidgetApp
"""

kivy.require('1.11.0')
# evtl nachher True oder 'auto'
Window.fullscreen = True
Window.borderless = True


color_text: str = '[color=cccccc]'
color_h_text: str = '[color=eeffaa]'
color_close: str = '[/color]'
italic_open: str = '[i]'
italic_close: str = '[/i]'

routeStr: str = '[i][color=44eeee]{}[/color][/i]'

font_size = 20


class MyEntry:
    label = None
    img_ok_path = None
    img_N_path = None
    destination = None
    from_stat = None
    to_stat = None
    connection_type = None
    departure: str = None
    arrival: str = None
    is_notifications: bool = None


class MyScreen(ScreenManager):
    fs: str  # fragmentshader for custom screen transition. Currently unused

    def load_shader(self):
        file = open('fragmentShader.vert', mode='r')
        self.fs = file.read()
        file.close()

    def __init__(self, **kwargs):
        self.load_shader()
        if 'transition' not in kwargs:
            self.transition = WipeTransition()  # ShaderTransition(fs=self.fs)
        super(ScreenManager, self).__init__(**kwargs)
        self.fbind('pos', self._update_pos)

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
        if my_entry.is_notifications:
            img.source = my_entry.img_N_path
        else:
            img.source = my_entry.img_ok_path
        img.size = img.texture_size
        img.pos_hint = {'x': 0, 'center_y': .5}
        new_entry.add_widget(img)

        # add label Label
        lbl_lbl = Label()
        lbl_lbl.id = 'lbl_lbl'
        lbl_lbl.size_hint = (0.4, None)
        lbl_lbl.markup = True
        if my_entry.is_notifications:
            lbl_lbl.text = (color_text + italic_open + '{} {}' + italic_close + color_close).format(my_entry.label,
                                                                                                    my_entry.destination)
        else:
            lbl_lbl.text = (color_text + '{} {}' + color_close).format(my_entry.label, my_entry.destination)
        lbl_lbl.font_size = font_size
        lbl_lbl.halign = 'left'
        lbl_lbl.valign = 'middle'
        # TODO fix workaround
        lbl_lbl.texture_size = Window.size
        lbl_lbl.text_size = Window.size
        lbl_lbl.size = Window.size
        lbl_lbl.shorten = True
        lbl_lbl.pos_hint = {'center_x': .65, 'center_y': .5}
        new_entry.add_widget(lbl_lbl)

        # add time Label
        time_lbl = Label()
        time_lbl.id = 'time_lbl'
        time_lbl.size_hint_x = 0.3
        time_lbl.markup = True
        if my_entry.is_notifications:
            time_lbl.text = (color_h_text + italic_open + '{}' + italic_close + color_close + ' >> ').format(
                my_entry.departure) + (color_h_text + italic_open + '{}' + italic_close + color_close).format(
                my_entry.arrival)
        else:
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
    settings_opened: bool = False

    def build(self):
        Logger.info("App.build:")
        Window.size = (480, 320)
        self.settings_cls = SettingsWithNoMenu
        # settings and config
        Model.start_str = "jijid"# self.config.get('MVG Widget', 'start')
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
        Logger.info("App.build_config: {0}".format(config))
        config.setdefaults('MVG Widget', {'start': 'Dachau', 'dest': 'Forschungszentrum', 'amount': 3, 'font_size': 20})

    def build_settings(self, settings):
        Logger.info("App.build_settings: {0}".format(settings))
        settings.add_json_panel('MVG Widget', self.config, 'settings.json')
        scr: Screen = self.screen.get_by_id('settingsscreen')
        scr.add_widget(settings)

        _al = AnchorLayout(padding=5, anchor_x='right', anchor_y='top')
        back: Button = Button(text="close",
                              background_color=(1, 1, 1, 1),
                              color=(1, 1, 1, 1),
                              size=(65, 40),
                              size_hint=(None, None))
        back.bind(on_release=self.close_settings)
        _al.add_widget(back)
        scr.add_widget(_al)

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

    def display_settings(self, settings):
        Logger.info("App.display_settings: {0}".format(settings))
        if self.settings_opened:
            return
        self.settings_opened = True
        self.screen.current = 'settingsscreen'
        return True

    def close_settings(self, settings=None):
        Logger.info("App.close_settings: {0}".format(settings))
        if not self.settings_opened:
            return
        self.settings_opened = False
        self.screen.current = 'screen1'
        self._update(-1)
        return True

    def _update(self, dt):
        Logger.info('App._update: updating data and view')
        if self.settings_opened:
            return
        self.time = time()
        # route update
        self.screen.set_route(Model.get_route())
        # connection update
        self.screen.get_by_id('bl').clear_widgets()
        _departures = Model.get_next_departures()
        for el in _departures:
            self.screen.add_entry(el)


if __name__ == '__main__':
    _mvgWidgetApp = MvgWidgetApp()
    _mvgWidgetApp.run()
