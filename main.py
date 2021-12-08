from kivy.app import App
from kivy.uix.widget import Widget


class ScreenManager(Widget):
    pass
class MentalMendingApp(App):
    def build(self):
        return ScreenManager()

if __name__ == '__main__':
    MentalMendingApp().run()