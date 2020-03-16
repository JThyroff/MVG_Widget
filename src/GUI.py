import kivy

kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.button import Label


# Inherit Kivy's App class which represents the window
# for our widgets
# HelloKivy inherits all the fields and methods
# from Kivy
class MvgWidgetApp(App):

    # This returns the content we want in the window
    def build(self):
        # Return a label widget with Hello Kivy
        # The name of the kv file has to be mvgwidget
        # minus the app part from this class to
        # match up properly
        return Label()
