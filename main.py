__version__ = '0.1'
""" A simple Color Game make with kivy """

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import random


class BoxLayoutGame(BoxLayout):
    """ BoxLayout called by kivy """
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
# Choose the game mode, by default: Colours Mode
    mode_game = "Colours Mode"

    def start(self):
        """ on_click start this method """
# Change the game mode (Colors Mode or Text Mode)
# Mix colors and texts
        random.shuffle(self.colors)
        random.shuffle(self.texts)
# Kivy buttons text
        color1 = self.ids['bt1']
        color1.color = self.colors[0]
        color1.text = self.texts[0]
        color2 = self.ids['bt2']
        color2.text = self.texts[1]
        color2.color = self.colors[1]
        color3 = self.ids['bt3']
        color3.color = self.colors[2]
        color3.text = self.texts[2]
        color4 = self.ids['bt4']
        color4.color = self.colors[3]
        color4.text = self.texts[3]

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
        points_kv = self.ids['points']
# Start the Game now
        if self.points_str == "":
            self.points_str = " "
        else:
            # Game already started: Count points (depends on the Game mode)
            if self.mode_game == "Colours Mode":
                # Colours Mode
                self.color_name_to_rgb(self.texts[self.number_random])
                if self.colors[nbr] == self.texts_test:
                    self.points += 1
                else:
                    self.no_points += 1
                points_kv.text = "Points " + str(self.points) +\
                                 "   Miss " + str(self.no_points)
            elif self.mode_game == "Text Mode":
                # Text Mode
                if nbr == self.number_random:
                    self.points += 1
                else:
                    self.no_points += 1
                points_kv.text = "Points " + str(self.points) +\
                                 "   Miss " + str(self.no_points)
            else:
                pass

    def restart(self):
        mode_game_kv = self.ids['spinner_game']
        self.points_kv = self.ids['points']
        if mode_game_kv.text != self.mode_game:
            self.points = 0
            self.no_points = -1
            self.points_kv.text = "Push a button for start"
            if self.mode_game == "Colours Mode":
                self.text = "Start Text Mode"
            elif self.mode_game == "Text Mode":
                self.text = "Start Colours Mode"
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


class ColorAndTextApp(App):
    """ Kivy App """
    def build(self):
        return BoxLayoutGame()


if __name__ == '__main__':
    ColorAndTextApp().run()
