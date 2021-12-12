
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.uix.spinner import Spinner

LabelBase.register(name='pixel', fn_regular='micellaneous/pixel.ttf')

activeBattles = []
newBattle = {}
class ToolBar(Screen):
    pass
class Form(Screen):
    pass
class MainHub(Screen):
    pass
class BossHub(Screen):
    pass
class FormBase(Widget):
    name_input = ObjectProperty(None)
    dropDown_button = ObjectProperty(None)
    emotionSelector = ObjectProperty(None)
    
    def name_selection(self):
        global newBattle
        newBattle['enemyName'] = self.name_input.text
        self.name_input.text = ''
        self.emotionSelector.emotion_selection()
        self.emotionSelector.text = 'Pick an emotion'
        print(self.name_input.text, newBattle)


class EmotionPicker(Spinner):

    def emotion_selection(self):
        global newBattle
        newBattle['emotion'] = self.text
        print(self.text, newBattle)

class MainHubBase(Widget):
    pass
class BossHubBase(Widget):
    pass


class MentalMendingApp(App):
    def build(self):
        sm = ScreenManager()
        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(Form(name='form'))
        sm.add_widget(MainHub(name='mainhub'))
        sm.add_widget(BossHub(name='bosshub'))
        return sm

    def load_page(self, screen_name):
        self.root.current = screen_name

    def new_battle(self):
        global activeBattles
        global newBattle
        activeBattles.append(newBattle)
        newBattle = {}
        self.load_page('mainhub')
        print(activeBattles)

    #   screen = Builder.load_string(screen_toolBar)
   

if __name__ == '__main__':
    MentalMendingApp().run()