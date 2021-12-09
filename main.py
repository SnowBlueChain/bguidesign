
from kivy.app import App
from kivy.uix import widget
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.lang import Builder, builder
from kivy.uix import button
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty 
from kivy.uix.screenmanager import CardTransition, FadeTransition, FallOutTransition, NoTransition, RiseInTransition, ScreenManager, Screen, SlideTransition, SwapTransition, WipeTransition
from kivymd.uix.button import MDRectangleFlatButton


class ToolBar(Screen):
    pass
class Form(Screen):
    pass
class MainHub(Screen):
    pass
class BossHub(Screen):
    pass


class MentalMendingApp(MDApp):
  
    def build(self):
        self.theme_cls.theme_style = "Light" # "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        self.theme_cls.primary_hue = '500'
        sm = ScreenManager()
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(Form(name='form'))
        sm.add_widget(MainHub(name='mainhub'))
        sm.add_widget(BossHub(name='bosshub'))
        return sm

    def load_page(self, screen_name):
        self.root.current = screen_name

    #   screen = Builder.load_string(screen_toolBar)
   

if __name__ == '__main__':
    MentalMendingApp().run()