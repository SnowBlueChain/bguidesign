
import os
from random import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core import text
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty, StringProperty, DictProperty, NumericProperty, BooleanProperty
from kivy.uix.spinner import Spinner
from random import randint
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Line
from kivy.core.audio import SoundLoader

LabelBase.register(name='pixel', fn_regular='micellaneous/pixel.ttf')

activeBattles = []
newBattle = {}
homescreen = ''
battlescreen = ''
currentBattle = {}
# def fully_qualified_path(filename):
#     path = os.path.dirname(os.path.abspath(__file__))
#     return os.path.join(path, filename)
jsonPath = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'localData/activeBattles.json')
store = JsonStore(jsonPath)


class ToolBar(Screen):
    pass

class MainHub(Screen):
    mainHubBase = ObjectProperty(None)
    pass
class MainHubBase(Widget):
    layout = ObjectProperty(None)
    global store

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
        # self.layout = ObjectProperty(None)
        # for storedBattles in store:
        #     storedBattle = store.get(storedBattles)
        #     print(storedBattle)
        #     activeBattles.append(storedBattle)
            # Clock.schedule_once(lambda dt: self.add_MainHubBattles())

    def add_MainHubBattles(self):   
        self.layout.clear_widgets()
        # store.clear()
        for battle in activeBattles:
           
            store.put(battle['enemyName'], enemyName=battle['enemyName'], emotion=battle['emotion']
            , enemyKey=battle['enemyKey'])
            emotionIconAux = 'icons/'+battle['enemyKey'][0] + battle['enemyKey'][1] + '64.png'
            btn = SelectEnemy(size_hint=(None, None), enemyName=battle['enemyName'], mainHubBase = self.layout
            , emotionIcon = emotionIconAux, battleData = battle)
            self.layout.add_widget(btn)
            # btn = Button(text=str(numIndex), width=80, size_hint=(None, None))
            # self.layout.add_widget(btn)
        # for battle in range(50):
        #     numIndex += 1
        #     btn = Button(text=str(numIndex), width=80, size_hint=(None, None))
        #     self.layout.add_widget(btn)
class SelectEnemy(RelativeLayout):
    enemyName = StringProperty(None)
    mainHubBase = ObjectProperty(None)
    emotionIcon = StringProperty(None)
    battleData = DictProperty(None)
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     btn = Button(text=self.mainText, width=80, size_hint=(None, None))
    #     self.add_widget(btn)
    pass

class BossHub(Screen):
    pass
class BossHubBase(Widget):
    pass
class Form(Screen):
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
        self.select_enemy(self.emotionSelector.text)
        self.emotionSelector.text = 'Pick an emotion'
        print(self.name_input.text, newBattle)
    
    def select_enemy(self, emotion):
        global newBattle
        enemyIndex = str(randint(0, 2))
        enemyLetter = self.select_enemyLetter(emotion)
        newBattle['enemyKey'] = enemyLetter + enemyIndex
    
    def select_enemyLetter(self, emotion):
        emotionStringAux = (emotion[0] + emotion[1]).upper()
        return emotionStringAux
    
    def getHomeScreen(self):
        ref_homeScreen = self.manager.get_screen('mainhub')
        self.homeScreen = ref_homeScreen

class EmotionPicker(Spinner):

    def emotion_selection(self):
        global newBattle
        newBattle['emotion'] = self.text
        print(self.text, newBattle)

class SelectEnemy(RelativeLayout):
    enemyName = StringProperty(None)
    mainHubBase = ObjectProperty(None)
    emotionIcon = StringProperty(None)
    battleData = DictProperty(None)
    pass

class BattleHub(Screen):
    battleHubBase = ObjectProperty(None)
    pass

class BattleHubBase(Widget):
    global currentBattle
    enemySource = StringProperty(None)
    emotionKey = StringProperty(None)
    enemyKey = StringProperty(None)
    enemy = ObjectProperty(None)
    hitBoolean = BooleanProperty(False)
    frameRefreshBoolean = BooleanProperty(False)

    time = 0.0
    rate = 0.1
    frame = 1
    currentFrame = 1
    cycleCounter = 0


    def initialize_battle(self):
        self.emotionKey = currentBattle['enemyKey'][0]+currentBattle['enemyKey'][1]
        self.enemyKey = currentBattle['enemyKey']


        self.emotionKey = 'AN'
        self.enemyKey = 'AN2'

    def update(self, dt):
        if self.hitBoolean == False:
            self.updateFrame(dt)
        elif self.hitBoolean == True:
            self.updateHitFrame(dt)
            

   
    def updateFrame(self, dt):
        path = os.path.join((os.path.dirname(os.path.abspath(__file__))), ("enemies/"+ self.emotionKey + '/' + self.enemyKey + '/' + self.enemyKey + '/frame'))
        enemySourceAux = 'atlas://' + path
       
        self.time += dt
        if (self.time > self.rate):
            self.time -= self.rate 
            
            if self.frame !=0:
                self.currentFrame = self.frame
            self.enemySource = enemySourceAux + str(self.frame)
            self.frame = self.currentFrame
            self.frame += 1
            
            self.cycleCounter += 1
            if (self.frame > 6):
                self.frame = 1

            if self.cycleCounter > 1:
                self.cycleCounter = 0
                self.frameRefreshBoolean = True


    def updateHitFrame(self, dt):
        path = os.path.join((os.path.dirname(os.path.abspath(__file__))), ("enemies/"+ self.emotionKey + '/' + self.enemyKey + '/' + self.enemyKey + '/frame'))
        enemySourceAux = 'atlas://' + path

        self.time += dt
        if (self.time > (self.rate / 4)):
            self.time -= (self.rate / 4)
            
           
            self.enemySource = enemySourceAux + str(self.currentFrame)
            self.frame += 1
            if (self.frame > 0):
                self.frame = 0
                self.cycleCounter += 1
            if self.cycleCounter > 0:
                self.cycleCounter = 0
                # self.frame = self.currentFrame
                self.hitBoolean = False

class BattleHubBaseAux(Widget):
    hitbox = ObjectProperty(None)
    lineBoolean = False
    line = ''
    touch_X = NumericProperty(0)
    touch_Y = NumericProperty(0)
    currentHitAudio = 1

    def on_touch_down(self, touch):
        if self.lineBoolean ==  False:
            color = (random(), 1, 1)
            with self.canvas:
                Color(*color, mode='hsv')
                
                if self.lineBoolean ==  False:
                    self.line = Line(points=(touch.x, touch.y), pointsize=5, width= 10, close= True)
                    self.lineBoolean = True
                self.line.close = True
                self.touch_X = touch.x
                self.touch_Y = touch.y
                touch.ud['line'] = self.line
        else:
            touch.ud['line'] = self.line
            self.touch_X = touch.x
            self.touch_Y = touch.y
            for i in range(3):
                touch.ud['line'].points += [touch.x, touch.y]
                self.clearTail(touch)

    def on_touch_move(self, touch):
        if touch.ud:
            self.line.close = False
            touch.ud['line'].points += [touch.x, touch.y]
            self.clearTail(touch)
            self.touch_X = touch.x
            self.touch_Y = touch.y
        if self.hitbox.collide_widget(self.parent.battleHubBase.enemy):
            if self.parent.battleHubBase.hitBoolean == False and  self.parent.battleHubBase.frameRefreshBoolean == True:
                self.parent.battleHubBase.hitBoolean = True
                self.parent.battleHubBase.frameRefreshBoolean = False
                self.hitAudio()
               
   
    def clearTail(self, touch):
        touch.ud['line'].points = touch.ud['line'].points[-10:]

    def hitAudio(self):
        if self.currentHitAudio > 9:
            self.currentHitAudio = 1
        soundPath = 'audio/hit/' + str(self.currentHitAudio) + '.wav'
        sound = SoundLoader.load(soundPath)
        sound.play()
        self.currentHitAudio += 1
class MentalMendingApp(App):

    def build(self):
        sm = ScreenManager()
        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(MainHub(name='mainhub'))
        sm.add_widget(Form(name='form'))
        sm.add_widget(BossHub(name='bosshub'))
        sm.add_widget(BattleHub(name='battlehub'))
        self.get_screens(sm)

       
        return sm

    def load_page(self, screen_name):
        self.root.current = screen_name
    
    def load_battle(self, battleData):
        global currentBattle
        global battlescreen

        currentBattle = battleData
        battlescreen.battleHubBase.initialize_battle()
        self.root.current = 'battlehub'
        Clock.schedule_interval(battlescreen.battleHubBase.update, 1.0/60.0)
        # Clock.schedule_interval(battlescreen.battleHubBase.update, 1.0/60.0)
        print(currentBattle)

    def new_battle(self):
        global activeBattles
        global newBattle
        global homescreen
        activeBattles.append(newBattle)
        newBattle = {}
        homescreen.mainHubBase.add_MainHubBattles()
        self.load_page('mainhub')
        print(activeBattles)
    
    def get_screens(self, sm):
        global homescreen
        global store
        global battlescreen
        homescreen = sm.get_screen('mainhub')
        battlescreen = sm.get_screen('battlehub')
        for storedBattles in store:
            storedBattle = store.get(storedBattles)
            print(storedBattle)
            activeBattles.append(storedBattle)
            homescreen.mainHubBase.add_MainHubBattles()

   

if __name__ == '__main__':
    MentalMendingApp().run()