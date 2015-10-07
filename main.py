""" A simple Color Game make with kivy """
__version__ = '0.2.4'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.uix.spinner import Spinner

import random


class BoxLayoutGame(BoxLayout):
    """ BoxLayout called by kivy """
    sound = SoundLoader.load('Single_Ply_Prison_Mastered.ogg')
    sound.loop = True
    sound.play()
# Text when the game start
    text = 'Push a button for start'

# Color: red, green, blue and yellow
    colour1 = [1, 0, 0, 1]
    colour2 = [0, 1, 0, 1]
    colour3 = [0, 0, 1, 1]
    colour4 = [1, 1, 0, 1]

    text1 = 'red'
    text2 = 'green'
    text3 = 'blue'
    text4 = 'yellow'

    colors = [colour1, colour2, colour3, colour4]
    texts = [text1, text2, text3, text4]

    texts_test = ""
# Used for mix colors and texts
    number_random = 0
# Used for count points
    points = 0
    no_points = 0
    points_str = ""
    points_kv = ""

# Choose the game mode, by default: Colours Mode
    mode_game = "Colours Mode"

    def start(self):
        """ on_click start this method """
# Change the game mode (Colors Mode or Text Mode)
# Mix colors and texts
        random.shuffle(self.colors)
        random.shuffle(self.texts)
# Kivy buttons text
        bt1 = self.ids['bt1']
        bt1.color = self.colors[0]
        bt1.text = self.texts[0]
        bt2 = self.ids['bt2']
        bt2.text = self.texts[1]
        bt2.color = self.colors[1]
        bt3 = self.ids['bt3']
        bt3.color = self.colors[2]
        bt3.text = self.texts[2]
        bt4 = self.ids['bt4']
        bt4.color = self.colors[3]
        bt4.text = self.texts[3]

    def ask(self):
        """ update question text """
        welcome = self.ids['welcome_text']
        self.number_random = random.randint(0, 3)
        self.text = 'Push the button ' +\
                    str(self.texts[self.number_random])
        self.restart()
        welcome.text = self.text

    def count_points(self, nbr):
        """ Count the points """
        self.points_kv = self.ids['points']
# Start the Game now
        if not self.points_str:
            self.points_str = " "
        else:
            # Game already started: Count points (depends on the Game mode)
            if self.mode_game == "Colours Mode":
                # Colours Mode
                self.color_name_to_rgb(self.texts[self.number_random])
                if self.colors[nbr] == self.texts_test:
                    self.points += 1
                    self.sound_points_play()
                else:
                    self.no_points += 1
                    BoxLayoutGame.sound_miss_play()
                self.points_kv.text = "Points " + str(self.points) +\
                                      "   Miss " + str(self.no_points)
            elif self.mode_game == "Text Mode":
                # Text Mode
                if nbr == self.number_random:
                    self.points += 1
                    self.sound_points_play()
                else:
                    self.no_points += 1
                    BoxLayoutGame.sound_miss_play()
                self.points_kv.text = "Points " + str(self.points) +\
                                      "   Miss " + str(self.no_points)
            else:
                pass

    def restart(self):
        """ Restart the game in another mode  """
        mode_game_kv = self.ids['spinner_game']
        self.points_kv = self.ids['points']
        if mode_game_kv.text != self.mode_game:
            self.points = 0
            self.no_points = 0
            self.points_kv.text = "Push a button for start"
            if self.mode_game == "Colours Mode":
                self.text = "Start Text Mode"
                self.points_str = ""
                self.points_kv.text = "Push on the good text"
            elif self.mode_game == "Text Mode":
                self.text = "Start Colours Mode"
                self.points_str = ""
                self.points_kv.text = "Push on the Good Color"
            else:
                pass
            self.mode_game = mode_game_kv.text
        else:
            pass

    def color_name_to_rgb(self, name):
        """ Change a name color to a rgb color """
# Replace Webcolors library
        if name == 'red':
            name = [1, 0, 0, 1]
        elif name == 'green':
            name = [0, 1, 0, 1]
        elif name == 'blue':
            name = [0, 0, 1, 1]
        elif name == 'yellow':
            name = [1, 1, 0, 1]
        else:
            pass
        self.texts_test = name

    @staticmethod
    def sound_miss_play():
        """ If no points: play miss sound """
        sound1 = SoundLoader.load('miss.ogg')
        sound1.play()

    @staticmethod
    def sound_points_play():
        """ If points: play point sound """
        sound1 = SoundLoader.load('points.ogg')
        sound1.play()

    @staticmethod
    def sound_play():
        """ When change mode (spinner): play point sound """
        sound1 = SoundLoader.load('change.ogg')
        sound1.play()

    def spinner_restart(self):
        """ Restart all text when click on spinner """
        welcome = self.ids['welcome_text']
        welcome.text = "Please push a button for start"
        points_kv = self.ids['points']
        self.points_str = ""
        points_kv.text = self.points_str
        self.no_points = 0
        self.points = 0
        self.sound.stop()
        self.sound.play()


class MyButton(Button):
    """ Custom Spinner Button """
    @staticmethod
    def sound():
        """ Play a sound when call by MyButton: kv file """
        sound_valid = SoundLoader.load("validation.ogg")
        sound_valid.play()


class MySpinner(Spinner):
    """ Custom Spinner """
    option_cls = ObjectProperty(MyButton)
    values = ListProperty()


class ColorAndTextApp(App):
    """ Kivy App """
    def build(self):
        return BoxLayoutGame()


if __name__ == '__main__':
    ColorAndTextApp().run()
