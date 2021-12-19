
import os
import math
from random import random
from kivy.vector import Vector
from kivy.app import App
from kivy.clock import Clock
from kivy.core import text
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty, StringProperty, DictProperty, NumericProperty, BooleanProperty, ReferenceListProperty
from kivy.uix.spinner import Spinner
from random import randint
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Line
from kivy.core.audio import SoundLoader
# from kivy.core.window import Window

# Window.size = (550, 650)

LabelBase.register(name='pixel', fn_regular='micellaneous/pixel.ttf')

activeBattles = []
newBattle = {}
homescreen = ''
battlescreen = ''
currentBattle = {}
currentIndex = -1
jsonPath = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'localData/activeBattles.json')
store = JsonStore(jsonPath)
clock = ''
finishEnemyBoolean = False

musicList = []
currentMusic = ''

for i in range (1, 4):
    musicSelector = i
    musicPath = 'audio/music/' + str(musicSelector) + '.wav'
    print('music', musicPath)
    backgroundMusic = SoundLoader.load(musicPath)
    backgroundMusic.loop = True

   
    musicList.append(backgroundMusic)
    print(musicList, 'aqui')
finalTouch = SoundLoader.load('audio/hit/gg.wav')



class ToolBar(Screen):
    pass

class MainHub(Screen):
    mainHubBase = ObjectProperty(None)
    pass
class MainHubBase(Widget):
    layout = ObjectProperty(None)
    global store

    def add_MainHubBattles(self):   
        self.layout.clear_widgets()
        for battle in activeBattles:
           
            store.put(battle['enemyName'], enemyName=battle['enemyName'], emotion=battle['emotion']
            , enemyKey=battle['enemyKey'])
            emotionIconAux = 'icons/'+battle['enemyKey'][0] + battle['enemyKey'][1] + '64.png'
            btn = SelectEnemy(size_hint=(None, None), enemyName=battle['enemyName'], mainHubBase = self.layout
            , emotionIcon = emotionIconAux, battleData = battle)
            self.layout.add_widget(btn)

class SelectEnemy(RelativeLayout):
    enemyName = StringProperty(None)
    mainHubBase = ObjectProperty(None)
    emotionIcon = StringProperty(None)
    battleData = DictProperty(None)
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
    mainHub = ObjectProperty(None)
    
    pass

class BattleHubBase(Widget):
    global currentBattle
    enemySource = StringProperty(None)
    enemyName = StringProperty(None)
    emotionKey = StringProperty(None)
    enemyKey = StringProperty(None)
    enemy = ObjectProperty(None)
    hitBoolean = BooleanProperty(False)
    frameRefreshBoolean = BooleanProperty(False)
    battleHubBaseAux = ObjectProperty(None)
    widgetToDelete = ObjectProperty(None)
    deleteBoolean = BooleanProperty(False)
    turnBoolean = BooleanProperty(True) #True = player turn, False = Enemy turn
    attackCompleted = BooleanProperty(False)
    shieldTransparency = NumericProperty(0)
    backgroundColorR = NumericProperty(0.95)
    backgroundColorG = NumericProperty(1)
    backgroundColorB = NumericProperty(1)
    hitA = NumericProperty(0)
    backgroundCycle = 0
    backgroundBoolean = False
    damageBoolean = False
    time = 0.0
    rate = 0.1
    frame = 1
    currentFrame = 1
    cycleCounter = 0


    def initialize_battle(self):
        global activeBattles
        print (activeBattles)
        global finishEnemyBoolean
        finishEnemyBoolean == False
        self.enemy.pos = (self.width/ 2.8, self.height /1.5)
        self.emotionKey = currentBattle['enemyKey'][0]+currentBattle['enemyKey'][1]
        self.enemyKey = currentBattle['enemyKey']
        self.enemyName = currentBattle['enemyName']

        # meanwhile we only have one enemy
        self.emotionKey = 'AN'
        self.enemyKey = 'AN2'

        
    def update(self, dt):
        global finishEnemyBoolean
        if finishEnemyBoolean == False:
            self.turnManager(dt)
            if self.hitBoolean == False:
                self.updateFrame(dt)
            elif self.hitBoolean == True:
                self.updateHitFrame(dt)
            if self.deleteBoolean == True:
                self.deleteWidget(self.widgetToDelete)
                self.deleteBoolean = False
        else:
            if self.hitBoolean == False:
                self.updateFrame(dt)
            elif self.hitBoolean == True:
                self.updateHitFrame(dt)
            self.checkDamage(dt)
   
    def checkChildren(self):
        if (len(self.children) <= 2) and self.turnBoolean == False:
            self.turnBoolean = True

    def deleteWidget(self, widget):
        self.remove_widget(widget)
        self.widgetToDelete = ObjectProperty(None)
                

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
        global finishEnemyBoolean
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
                self.hitBoolean = False
    
    def turnManager(self, dt): 
        if self.turnBoolean == False:
           self.startAttackAnimation(dt)
           
           
        if self.turnBoolean == True:
            self.hitA = 0
            self.startPlayerTurn()
            

    def startPlayerTurn(self):
        # self.turnBoolean = True
        self.battleHubBaseAux.buttonsBoolean = True
        if self.battleHubBaseAux.hideButtons == 0:
            self.battleHubBaseAux.hideButtons = 1
            self.battleHubBaseAux.endFight.text = 'End It!'
            self.battleHubBaseAux.pauseFight.text = 'Pause'
        self.attackCompleted = False
        self.shieldTransparency = 0
        self.damageBoolean = False

    def enemyAttack(self, dt):
        if self.attackCompleted == False:
            
            for i in range(1, 8):
                directionAux = 1
                initial_xAux = 10
                if i % 2 == 0:
                    directionAux = -1
                    initial_xAux = 500
                projectile = enemyAttack(source='icons/AN64.png' ,initial_y = (i*50) ,
                movement= 2, initial_x = initial_xAux, x_speed = i /2,
                 direction = directionAux)
                self.add_widget(projectile)
                Clock.schedule_interval(projectile.bulletUpdate, 1.0/60.0)
        
        else:
            self.checkChildren()
            self.checkDamage(dt)
        
        self.attackCompleted = True

    backgroundCycleCounter = 0
    def startAttackAnimation(self, dt):
        if self.backgroundBoolean == True:
            if self.backgroundCycle == 0:
                self.backgroundColorB -=0.02 * 100 * dt
                if self.backgroundColorB <= 0.5:
                    self.backgroundCycle = 1
                    self.backgroundCycleCounter += 1
                    
            if self.backgroundCycle == 1:
                self.backgroundColorB +=0.02 * 100 * dt
                if self.backgroundColorB >= 1:
                    self.backgroundCycle = 0
                    self.backgroundCycleCounter += 1
            if self.backgroundCycleCounter >= 6:
                self.backgroundBoolean = False
                self.backgroundCycleCounter = 0     
        else:
            self.enemyAttack(dt)
            

    damageCycle = 0
    damageCycleCounter = 0

    def checkDamage(self, dt):
        if self.damageBoolean == True:
            if self.damageCycle == 0:
                self.hitA +=0.03 * 100 * dt
                if self.hitA >= 0.5:
                    self.damageCycle = 1
                    self.damageCycleCounter += 1
                    
            if self.damageCycleCounter == 1:
                self.hitA -=0.03 * 100 * dt
                if self.hitA <= 0.0:
                    self.damageCycle = 0
                    self.damageCycleCounter += 1
            if self.damageCycleCounter >= 2:
                self.damageBoolean = False
                self.damageCycleCounter = 0

bulletHitAudioCounter = 1
class enemyAttack(Image):
    id = StringProperty(None)
    vel_X = NumericProperty(0)
    vel_Y = NumericProperty(0)
    vel = ReferenceListProperty(vel_X, vel_Y)
    movement = NumericProperty(0)
    initial_x = NumericProperty(0)
    initial_y= NumericProperty(0)
    x_speed = NumericProperty(0)
    direction = NumericProperty(0)
    time = 0.0
    rate = 0.03


    def bulletUpdate(self, dt):
        self.time += dt
        if (self.time > self.rate):
            self.time -= self.rate 
            if self.movement == 1:
                self.linearMovement()
            if self.movement == 2:
                self.sinMovement(dt)
        self.removeBullet()
            
        
    def removeBullet(self):
        if self.parent:
            if self.parent.battleHubBaseAux.hitbox.collide_widget(self):
                if self.parent.damageBoolean == False:
                    self.parent.damageBoolean = True
                    self.playerHitAudio()
                self.parent.widgetToDelete = self
                self.parent.deleteBoolean = True
            # this two make the bullet dissappear when touching the borders of the screen
            if self.x > self.parent.width or self.x < self.parent.x:
                self.parent.widgetToDelete = self
                self.parent.deleteBoolean = True
            if self.top > self.parent.top or self.y < self.parent.y:
                self.parent.widgetToDelete = self
                self.parent.deleteBoolean = True
    

    def linearMovement(self):
        self.pos = Vector(*self.vel) + self.pos
    
    def sinMovement(self, dt):
        y_value =  (100*math.sin(self.initial_x/20 - 10) +self.initial_y)
        self.pos = Vector(self.initial_x, y_value)
        self.initial_x += self.x_speed * self.direction * dt * 50

    def playerHitAudio(self):
        global bulletHitAudioCounter
        if bulletHitAudioCounter > 3:
            bulletHitAudioCounter = 1
        soundPath = 'audio/playerHit/' + str(bulletHitAudioCounter) + '.wav'
        sound = SoundLoader.load(soundPath)
        sound.play()
        bulletHitAudioCounter += 1




        
        
class BattleHubBaseAux(Widget):
    hitbox = ObjectProperty(None)
    lineBoolean = False
    line = ObjectProperty(None)
    touch_X = NumericProperty(0)
    touch_Y = NumericProperty(0)
    currentHitAudio = 1
    currentShieldHitAudio = 1
    hitCounter = 0
    pauseFight = ObjectProperty(None)
    endFight = ObjectProperty(None)
    buttonsBoolean = ObjectProperty(True)
    hideButtons = NumericProperty(0)

 


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
        if self.buttonsBoolean == True:
            if self.endFight.collide_widget(self.hitbox):
                self.finishFight()
            if self.pauseFight.collide_widget(self.hitbox):
                self.stopFight()

    def on_touch_move(self, touch):
        if touch.ud:
            self.line.close = False
            touch.ud['line'].points += [touch.x, touch.y]
            self.clearTail(touch)
            self.touch_X = touch.x
            self.touch_Y = touch.y
        self.collisionWithEnemy()

    def collisionWithEnemy(self):
        global finishEnemyBoolean
        if self.hitbox.collide_widget(self.parent.battleHubBase.enemy):
            if self.parent.battleHubBase.turnBoolean == True:
                if self.parent.battleHubBase.hitBoolean == False and  self.parent.battleHubBase.frameRefreshBoolean == True:
                    self.parent.battleHubBase.hitBoolean = True
                    self.parent.battleHubBase.frameRefreshBoolean = False
                    self.hitAudio()
                    if finishEnemyBoolean == False:
                        self.endPlayerTurn()
            elif self.parent.battleHubBase.frameRefreshBoolean == True:
                if finishEnemyBoolean == False:
                    self.parent.battleHubBase.frameRefreshBoolean = False
                    self.shieldHit()
                    if self.parent.battleHubBase.shieldTransparency <= 0.7:
                        self.parent.battleHubBase.shieldTransparency +=0.1 
                    Clock.schedule_once(self.shieldAnimation, 3)
               
   
    def clearTail(self, touch):
        touch.ud['line'].points = touch.ud['line'].points[-10:]

    
    finishFightCycle = 0
    def hitAudio(self):
        global finishEnemyBoolean
        global finalTouch
        if finishEnemyBoolean == False:
            if self.currentHitAudio > 9:
                self.currentHitAudio = 1
            soundPath = 'audio/hit/' + str(self.currentHitAudio) + '.wav'
            sound = SoundLoader.load(soundPath)
            sound.play()
            self.currentHitAudio += 1
        else: 
            if self.finishFightCycle < 3:
                if self.currentHitAudio > 9:
                    self.currentHitAudio = 1
                    self.finishFightCycle += 1
                  
            else:
                self.currentHitAudio = 9
                self.finishFightCycle += 1
            soundPath = 'audio/hit/' + str(self.currentHitAudio) + '.wav'
            sound = SoundLoader.load(soundPath)
            sound.play()
            
            if finalTouch.get_pos() == 0:
                if self.finishFightCycle == 5:
                    finalTouch.play()
                elif  self.finishFightCycle > 10 and finalTouch.state == 'stop':
                    self.stopFight()

            self.parent.battleHubBase.damageBoolean = True
            self.currentHitAudio += 1
            posx = self.parent.battleHubBase.enemy.pos[0]
            posy = self.parent.battleHubBase.enemy.pos[1]
            posx = randint(math.floor(posx - 50), math.floor(posx +50))
            posy = randint(math.floor(posy - 50), math.floor(posy +50))
            if posx > self.parent.battleHubBase.width -100 or posx < self.parent.battleHubBase.pos[0] +100:
                posx = self.parent.battleHubBase.width/ 2.8
            if posy > self.parent.battleHubBase.height -100 or posy < self.parent.battleHubBase.pos[1] +100:
                posy = self.parent.battleHubBase.height /1.5
            self.parent.battleHubBase.enemy.pos = (posx, posy)

       
    def shieldAnimation(self, dt):
        if self.parent.battleHubBase.shieldTransparency >= 0.5:
            self.parent.battleHubBase.shieldTransparency -=0.2 

    
    def shieldHit(self):
        if self.currentShieldHitAudio > 2:
            self.currentShieldHitAudio = 1
        soundPath = 'audio/shieldHit/' + str(self.currentShieldHitAudio) + '.wav'
        sound = SoundLoader.load(soundPath)
        sound.play()
        self.currentShieldHitAudio +=1
        

    def endPlayerTurn(self):
        global finishEnemyBoolean
        if self.hitCounter > 8:
            self.hitCounter = 0
        self.hitCounter += 1
        if self.parent.battleHubBase.turnBoolean == True and self.hitCounter > 8:
            self.hideButton()
            self.parent.battleHubBase.turnBoolean = False
            self.parent.battleHubBase.backgroundBoolean = True
            if finishEnemyBoolean == False:
                Clock.schedule_once(self.deployShield, 1)


    def deployShield(self, dt):
        self.parent.battleHubBase.shieldTransparency = 0.5

    def hideButton(self):
        self.buttonsBoolean = False
        self.hideButtons = 0
        self.endFight.text = ''
        self.pauseFight.text = ''

    
    def stopFight(self):
        global currentMusic
        global clock
        global store
        global activeBattles
        global currentIndex
        global homescreen
        currentMusic.stop()
        global finishEnemyBoolean
        if finishEnemyBoolean == True:
            store.delete(self.parent.battleHubBase.enemyName)
            del activeBattles[currentIndex]
            homescreen.mainHubBase.add_MainHubBattles()
            
            
        finishEnemyBoolean = False
        self.parent.parent.current = 'mainhub'
        
        self.parent.battleHubBase.cycleCounter = 0
        self.finishFightCycle = 0
        clock.cancel()
    
    def finishFight(self):
        global finishEnemyBoolean
        finishEnemyBoolean = True
        self.hideButton()
        


    
clockBoolean = False
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
        global activeBattles
        global currentIndex

        currentBattle = battleData
        currentIndex = activeBattles.index(battleData)
        print (currentIndex)
        battlescreen.battleHubBase.initialize_battle()
        self.root.current = 'battlehub'
        global clock 
        clock = Clock.schedule_interval(battlescreen.battleHubBase.update, 1.0/60.0)
        
        Clock.schedule_once(self.startMusic, 0)

        print(currentBattle)
        
    def startMusic(self, dt):
        i = randint(0, 2)
        global musicList
        global currentMusic
        currentMusic = musicList[i]
        musicList[i].play()

    
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