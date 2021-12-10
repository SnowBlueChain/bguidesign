
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import NoTransition, RiseInTransition, ScreenManager, Screen, SlideTransition, SwapTransition, WipeTransition


class ToolBar(Screen):
    pass
class Form(Screen):
    pass
class MainHub(Screen):
    pass
class BossHub(Screen):
    pass
class FormBase(Widget):
    pass


class MentalMendingApp(App):
  
    def build(self):
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