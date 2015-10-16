# -*- coding: utf-8 -*-
""" A simple Color Game made with kivy """
__version__ = '0.4.1'

from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from plyer import vibrator
from kivy.utils import platform

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

import random
import time


class MenuScreen(Screen):
    """ BoxLayout called by kivy """
    # Music On Menu Screen
    # sound = SoundLoader.load('BCG-01.ogg')
    # sound.loop = True
    # sound.play()

    @staticmethod
    def leave():
        """ Leave the apps """
        App.get_running_app().stop()

    def start_text_mode(self):
        """ show_popup: start Text Mode """
        GameScreen.mode_game = "Text Mode"

    def start_color_mode(self):
        """ show_popup: start Colours Mode """
        GameScreen.mode_game = "Colours Mode"

    @staticmethod
    def sound_validation():
        """ Play a sound when call by MyButton: kv file """
        sound_valid = SoundLoader.load("validation.ogg")
        sound_valid.play()


class GameScreen(Screen):
    """ BoxLayout called by kivy """
    # Music during the game
    sound_game = SoundLoader.load('BCG-01.ogg')
    sound_game.loop = True
    sound_game.play()
    # see get_time_final
    sound_win = SoundLoader.load("win.ogg")
    # Mute or unmute the Music, see active
    sound_pos = "unmute"
    # Text when the game start
    text = 'Push a button for start'
    # Color: rouge, vert, bleu and jaune
    colour1 = [1, 0, 0, 1]
    colour2 = [0, 1, 0.2, 1]
    colour3 = [0, 0, 1, 1]
    colour4 = [1, 1, 0, 1]

    text1 = 'rouge'
    text2 = 'vert'
    text3 = 'bleu'
    text4 = 'jaune'

    colors = [colour1, colour2, colour3, colour4]
    texts = [text1, text2, text3, text4]

    texts_test = ""
    # Used for mix colors and texts
    number_random = 0
    # Used for count points
    points = NumericProperty(0)
    no_points = NumericProperty(0)
    # start the game
    points_str = ""

    # Choose the game mode, by default: Colours Mode
    mode_game = StringProperty(None)
    old_mode_game = ""
    # Time
    time_1 = ""
    time_2 = 0
    time_penality = 0
    # time_2 - time1
    t_final = ""
    t_final_no_penality = 0
    # best time final
    t_best = 100.
    records = "New Records = "
    # 0/1 time mode active/disable
    time_mode = 0
    # Switch active: active/disable time mode
    active = False
    # ProgressBar for time mode
    progress_bar_1 = ObjectProperty(None)
    value_progress_bar = 0

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        # if platform == 'linux':
        #     box = BoxLayout'
        self.post_build_init()

    def get_time_1(self):
        """ Used for start chronometer  """
        self.time_1 = time.time()

    def get_time_2(self):
        """ Used for end chronometer """
        self.time_2 = time.time()

    def get_time_final(self):
        """ chronometer time """
        self.t_final = (self.time_2 + float(self.time_penality)) - self.time_1
        self.t_final_no_penality = self.time_2 - self.time_1
        self.t_final_no_penality = "%.2F" % self.t_final_no_penality
        self.t_final = "%.2f" % self.t_final
        if float(self.t_final) < float(self.t_best):
            self.t_best = self.t_final
            self.records = "New Records !!! "
            self.sound_win.play()
            self.sound_game.stop()
        else:
            self.records = "Best Records = "
            self.sound_validation()

    def replay(self):
        """ Button replay """
        self.value_progress_bar = 0
        try:
            self.progress_bar_1.value = self.value_progress_bar
        except AttributeError:
            pass
        try:
            points_kv = GameScreen.ids['points']
        except TypeError:
            pass
        self.points = 0
        self.no_points = 0
        self.time_penality = 0
        try:
            points_kv.text = ""
        except UnboundLocalError:
            pass
        self.ask()
        self.time_1 = ""
        pts_kv = self.ids['points']
        pts_kv.text = ""
        # self.sound_win.stop()
        # self.sound_game.play()

    def ask(self):
        """ update question text """
        try:
            welcome = self.ids['welcome_text']
        except KeyError:
            pass
        self.number_random = random.randint(0, 3)
        self.text = 'Push the button ' +\
                    str(self.texts[self.number_random])
        try:
            welcome.text = self.text
        except UnboundLocalError:
            pass

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

    def count_points(self, nbr):
        """ Count the points """
        points_kv = self.ids['points']
        # progress_bar = self.ids['progress']
        # Start the Game now
        if not self.points_str:
            self.points_str = " "
        else:
            # Game already started: Count points (depends on the Game mode)
            if not self.time_1:
                self.get_time_1()
            else:
                pass
            if self.mode_game == "Colours Mode":
                # Colours Mode
                self.color_name_to_rgb(self.texts[self.number_random])
                if self.colors[nbr] == self.texts_test:
                    # Win
                    self.points += 500
                    if self.active is True:
                        # time mode active
                        self.value_progress_bar += 50
                    else:
                        pass
                    self.sound_points_play()
                else:
                    # Miss
                    self.no_points += 1
                    self.time_penality += 3
                    # On Android
                    try:
                        vibrator.vibrate(0.4)
                    except NotImplementedError:
                        pass
                    self.sound_miss_play()
                points_kv.text = "Points " + str(self.points) +\
                                 "   Miss " + str(self.no_points)
                try:
                    self.progress_bar_1.value = self.value_progress_bar
                except AttributeError:
                    pass
            elif self.mode_game == "Text Mode":
                # Text Mode
                if nbr == self.number_random:
                    # Win
                    self.points += 50
                    if self.active is True:
                        # time mode active
                        self.value_progress_bar += 3
                    else:
                        pass
                    self.sound_points_play()
                else:
                    self.no_points += 1
                    self.time_penality += 3
                    GameScreen.sound_miss_play()
                    # On Android
                    try:
                        vibrator.vibrate(0.4)
                    except NotImplementedError:
                        pass
                try:
                    self.progress_bar_1.value = self.value_progress_bar
                except AttributeError:
                    pass

                points_kv.text = "Points " + str(self.points) +\
                                 "   Miss " + str(self.no_points)
                # progress_bar.value = self.value_progress_bar
            else:
                pass
            if self.value_progress_bar >= 99:
                # progress_bar.value = self.value_progress_bar
                self.get_time_2()
                self.get_time_final()
                self.change_text()
                self.value_progress_bar = 0
                self.manager.current = 'win'
                self.replay()
            else:
                pass
            if self.manager.current == 'win':
                self.sound_win.play()
            else:
                self.sound_win.stop()
                self.sound_game.play()

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
        """ When change mode: play point sound """
        sound1 = SoundLoader.load('change.ogg')
        sound1.play()

    @staticmethod
    def sound_validation():
        """ Play a sound when call by MyButton: kv file """
        sound_valid = SoundLoader.load("validation.ogg")
        sound_valid.play()

    def color_name_to_rgb(self, name):
        """ Change a name color to a rgb color """
        # Replace Webcolors library
        if name == 'rouge':
            name = [1, 0, 0, 1]
        elif name == 'vert':
            name = [0, 1, 0.2, 1]
        elif name == 'bleu':
            name = [0, 0, 1, 1]
        elif name == 'jaune':
            name = [1, 1, 0, 1]
        else:
            pass
        self.texts_test = name

    def post_build_init(self):
        """ import BACK_KEY from Android """
        if platform() == 'android':
            import android
            android.map_key(android.KEYCODE_BACK, 1001)

        win = Window
        win.bind(on_keyboard=self.key_handler)

    def key_handler(self, window, keycode1, keycode2, text, modifiers):
        """ On push Back_key: run go_start (popup) """
        if keycode1 == 27 or keycode1 == 1001:
            self.replay()
            # Returning True will eat the keypress
            if self.manager.current == 'menu':
                MenuScreen.leave()
            self.manager.current = 'menu'
            return True
        return False

    def on_pause(self):
        """ Enable pause on mobile """
        return True

    def change_time_mode(self):
        """ Enable or Disable time_mode """
        if self.time_mode == 0:
            self.progress_bar_1 = ProgressBar(id='progress',
                                              value=self.value_progress_bar,
                                              size_hint_y=0.1)
            self.time_mode = 1
            self.active = True
            self.add_widget(self.progress_bar_1)
        else:
            self.time_mode = 0
            self.active = False
            self.remove_widget(self.progress_bar_1)
        if not self.points_str:
            pass
        else:
            self.replay()

    @staticmethod
    def self_active():
        """ Mute/Unmute """
        if GameScreen.sound_pos == "unmute":
            GameScreen.sound_pos = "mute"
            GameScreen.sound_game.volume = 0
        elif GameScreen.sound_pos == "mute":
            GameScreen.sound_pos = "unmute"
            GameScreen.sound_game.volume = 1

    def change_text(self):
        """Not used """
        # label_3 = WinScreen().ids['label_3']
        # label_3.text = "ok"


class WinScreen(Screen):
    """ On Win: Progress_bar """
    text1 = str(GameScreen.points)
    text2 = StringProperty("")
    text3 = StringProperty("")
    text4 = StringProperty("")
    text5 = StringProperty("")
    text6 = StringProperty("")


class BrainColorGame(App):
    """ Main App """
    # t_final_no_penality
    text_2 = StringProperty('')
    # no_points
    text_3 = StringProperty('')
    # time_penality
    text_4 = StringProperty('')
    # t_final
    text_5 = StringProperty('')
    # records + t_brest
    text_6 = StringProperty('')

    def build(self):
        """ Use ScreenManager """
        self.bind(text_2=self.update)
        # Create the screen manager
        sm = ScreenManager()
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(WinScreen(name='win'))
        return sm

    def update(self, *args):
        """ build self.bind """
        print "whatever"

if __name__ == '__main__':
    BrainColorGame().run()
