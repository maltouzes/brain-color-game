""" A simple Color Game make with kivy """

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import random


class BoxLayoutGame(BoxLayout):
    """ BoxLayout called by kivy """

    text = 'Cliquez pour commencer'
    colour1 = [1, 0, 0, 1]
    colour2 = [0, 1, 0, 1]
    colour3 = [0, 0, 1, 1]
    colour4 = [1, 1, 0, 1]

    text1 = 'rouge'
    text2 = 'vert'
    text3 = 'bleu'
    text4 = 'jaune'

    colors = [colour1, colour2, colour3, colour4]

    texts = [text1, text2, text3, text4]

    def start(self, *args):
        """ on_click start this method """
        random.shuffle(self.colors)
        random.shuffle(self.texts)

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

        print self.colors
        print self.texts

        welcome = self.ids['welcome_text']
        number_random = random.randint(0, 3)
        print number_random
        self.text = 'Cliquez sur le bouton ' + str(self.texts[number_random])
        welcome.text = self.text


class ColorAndTextApp(App):
    """ Kivy App """
    def build(self):
        return BoxLayoutGame()


if __name__ == '__main__':
    ColorAndTextApp().run()
