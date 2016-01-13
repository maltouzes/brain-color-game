# -*- coding: utf-8 -*-
""" A simple Color Game made with kivy """
__version__ = '0.5.14'

from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from plyer import vibrator
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.settings import SettingsWithNoMenu
from kivy.uix.image import Image
import random
import time
import os
Window.size = (480, 800)


class Buttonmy(ButtonBehavior, Label):
    """ My custon button """
    # def on_press(self):
    # print("on_press")
    pass


class ButtonHelp(ButtonBehavior, Image):
    pass


class ButtonSound(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ButtonSound, self).__init__(**kwargs)
        self.bind(state=self.state_changed)

    def state_changed(self, *args):
        """ Change the img source when the button is pressed """
        print GameScreen.active
        if BrainColorGame.sound_game.volume == 0:
            self.source = (os.getcwd() + "/sound_on_off1.png")
        else:
            self.source = (os.getcwd() + "/sound_off_on1.png")


class ButtonColorWord(ButtonBehavior, Image):
    pass


class ButtonOk(ButtonBehavior, Image):
    """ Custon Ok Button """
    def __init__(self, **kwargs):
        super(ButtonOk, self).__init__(**kwargs)
        self.bind(state=self.state_changed)

    def state_changed(self, *args):
        """ Change the img source when the button is pressed """
        if self.source == (os.getcwd() + "/Button-Ok-push.png"):
            self.source = (os.getcwd() + "/Button-Ok.png")
        else:
            self.source = (os.getcwd() + "/Button-Ok-push.png")
            pass


class ButtonMenuRepeat(ButtonBehavior, Image):
    pass


class ButtonColours(ButtonBehavior, Image):
    """ My custon Image Button """
    def __init__(self, **kwargs):
        super(ButtonColours, self).__init__(**kwargs)
        self.bind(state=self.state_changed)

    def state_changed(self, *args):
        """ Change the img source when the button is pressed """
        if self.source == (os.getcwd() + "/Button_yellow.png"):
            self.source = (os.getcwd() + "/Button_purple.png")
        else:
            self.source = (os.getcwd() + "/Button_yellow.png")
            pass


class ButtonText(ButtonBehavior, Image):
    """ My custon Image Button """
    def __init__(self, **kwargs):
        super(ButtonText, self).__init__(**kwargs)
        self.bind(state=self.state_changed)

    def state_changed(self, *args):
        """ Change the img source when the button is pressed """
        if self.source == (os.getcwd() + "/Button_yellow.png"):
            self.source = (os.getcwd() + "/Button_purple.png")
        else:
            self.source = (os.getcwd() + "/Button_yellow.png")


class ButtonExit(ButtonBehavior, Image):
    """ My Custom Exit Button """
    pass


class StartScreen(Screen):
    @staticmethod
    def leave():
        """ Leave the apps """
        App.get_running_app().stop()


class MenuScreen(Screen):
    """ BoxLayout called by kivy """
    @staticmethod
    def leave():
        """ Leave the apps """
        App.get_running_app().stop()

    @staticmethod
    def start_text_mode():
        """ show_popup: start Text Mode """
        GameScreen.mode_game = "Text Mode"

    @staticmethod
    def start_color_mode():
        """ show_popup: start Colours Mode """
        GameScreen.mode_game = "Colours Mode"

    @staticmethod
    def sound_validation():
        """ Play a sound when call by MyButton: kv file """
        sound_valid = SoundLoader.load("validation.ogg")
        sound_valid.play()


class GameScreen(Screen):
    """ BoxLayout called by kivy """
    sound_pos = "unmute"
    # Text when the game start
    text = 'Push a button for start'
    text_button = "Push a button"
    # Color: rouge, vert, bleu and jaune
    colour1 = [1, 0, 0, 1]
    # colour2 = [0, 1, 0.2, 1]
    colour2 = [0.02, 0.898, 0.2, 1]
    colour3 = [0, 0, 1, 1]
    colour4 = [1, 1, 0, 1]

    text1 = 'rouge'
    text2 = 'vert'
    text3 = 'bleu'
    text4 = 'jaune'

    colors = [colour1, colour2, colour3, colour4]
    texts = [text1, text2, text3, text4]

    colors_dict = {'rouge': [1, 0, 0, 1],
                   'vert': [0.02, 0.898, 0.2, 1],
                   'bleu': [0, 0, 1, 1],
                   'jaune': [1, 1, 0, 1]}

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
    score_file = os.getcwd() + "/scores_bcg"
    score_file_color = os.getcwd() + "/scores_color_bcg"
    score_file_text = os.getcwd() + "/scores_text_bcg"
    t_best = 999.
    t_best_color = 999.
    t_best_text = 999.
    records = "New Records = "
    t_best_mode = ObjectProperty(None)
    # 0/1 time mode active/disable
    time_mode = 0
    # Switch active: active/disable time mode
    active = False
    # ProgressBar for time mode
    progress_bar_1 = ObjectProperty(None)
    value_progress_bar = 0

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.post_build_init()

    def get_time_1(self):
        """ Used for start chronometer  """
        self.time_1 = time.time()

    def get_time_2(self):
        """ Used for end chronometer """
        self.time_2 = time.time()

    def get_time_final(self, mode):
        """ chronometer time """
        self.t_final = (self.time_2 + float(self.time_penality)) - self.time_1
        self.t_final_no_penality = self.time_2 - self.time_1
        self.t_final_no_penality = "%.2F" % self.t_final_no_penality
        self.t_final = "%.2f" % self.t_final
        self.compare_time_final(mode)

    def compare_time_final(self, mode):
        """ Compare saved time and t_final """
        if mode == "Colours Mode":
            try:
                self.open_file(self.score_file_color, mode)
            except IOError:
                pass
            # t_best depend of the mode
            self.t_best = self.t_best_color
            if float(self.t_final) < float(self.t_best_color):
                self.t_best_color = self.t_final
                self.t_best = self.t_best_color
                self.save_new_record(self.score_file_color, self.t_best_color)
            else:
                self.no_new_record()
        elif mode == "Text Mode":
            try:
                self.open_file(self.score_file_text, mode)
            except IOError:
                pass
            # t_best depend of the mode
            self.t_best = self.t_best_text
            if float(self.t_final) < float(self.t_best_text):
                self.t_best_text = self.t_final
                self.t_best = self.t_best_text
                self.save_new_record(self.score_file_text, self.t_best_text)
            else:
                self.no_new_record()

    def open_file(self, score_file_mode, mode):
        """ Open scores file """
        file_saved = open(score_file_mode, 'r')
        scr = file_saved.read()
        scr = float(scr)
        if "Colour" in mode:
            self.t_best_color = scr
        else:
            self.t_best_text = scr

        file_saved.close()

    def no_new_record(self):
        """ if t_final >= t_best_mode """
        self.records = "Best Records = "
        self.sound_validation()

    def save_new_record(self, score_file_mode, t_best_mode):
        """ save scores in file: mode = text or color """
        self.records = "New Records !!! "
        file_saved = open(score_file_mode, 'w')
        file_saved.write(str(t_best_mode))
        file_saved.close()

    def replay(self):
        """ Button replay """
        self.text = ""
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
        welcome1 = self.ids['welcome_text']
        welcome1.text = "Push on the good Button"

    def ask(self):
        """ update question text """
        try:
            welcome = self.ids['welcome_text']
            bt_q = self.ids['bt_q']
        except KeyError:
            pass
        # Better than: self.number_random = random.randint(0, 3)
        self.number_random = int(random.choice('0123'))
        if GameScreen.mode_game == "Colours Mode":
            self.text = 'Push on the good color'
        elif GameScreen.mode_game == "Text Mode":
            self.text = 'Push on the Good Text'
        else:
            pass
        self.text_button = str(self.texts[self.number_random])
        try:
            welcome.text = self.text
            bt_q.text = self.text_button
            # bt_q.source = ("/home/user/Programmes/brain-color-game3/
            # brain-color-game/" +
            # str(self.text_button))
        except UnboundLocalError:
            pass

    def start(self):
        """ on_click start this method """
        # Change the game mode (Colors Mode or Text Mode)
        # Mix colors and texts
        random.shuffle(self.colors)
        random.shuffle(self.texts)
        # Kivy buttons text
        bt1b = self.ids['bt1b']
        bt1b.color = self.colors[0]
        bt1b.text = self.texts[0]
        bt1 = self.ids['bt1']
        # bt1.color = self.colors[0]
        bt1.text = self.texts[0]
        bt2b = self.ids['bt2b']
        bt2b.color = self.colors[1]
        bt2b.text = self.texts[1]
        bt2 = self.ids['bt2']
        # bt2.color = self.colors[1]
        bt2.text = self.texts[1]
        bt3b = self.ids['bt3b']
        bt3b.color = self.colors[2]
        bt3b.text = self.texts[2]
        bt3 = self.ids['bt3']
        # bt3.color = self.colors[2]
        bt3.text = self.texts[2]
        bt4b = self.ids['bt4b']
        bt4b.color = self.colors[3]
        bt4b.text = self.texts[3]
        bt4 = self.ids['bt4']
        # bt4.color = self.colors[3]
        bt4.text = self.texts[3]

    def count_points_good(self):
        """ Called by count_points """
        self.points += 50
        if self.active is True:
            self.value_progress_bar += 3
        else:
            pass
        self.sound_points_play()
        try:
            self.progress_bar_1.value = self.value_progress_bar
        except AttributeError:
            pass

    def count_points_false(self):
        """ Called by count_points """
        self.no_points += 1
        self.time_penality += 3
        self.sound_miss_play()
        # On Android
        try:
            vibrator.vibrate(0.4)
        except NotImplementedError:
            pass

    def count_points(self, nbr):
        """ Count the points """
        points_kv = self.ids['points']
        # progress_bar = self.ids['progress']
        # Start the Game now
        if not self.points_str or nbr == 5:
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
                    self.count_points_good()
                else:
                    # Miss
                    self.count_points_false()
            elif self.mode_game == "Text Mode":
                # Text Mode
                if nbr == self.number_random:
                    # Win
                    self.count_points_good()
                else:
                    # Miss
                    self.count_points_false()

            else:
                pass
            points_kv.text = "Points " + str(self.points) +\
                             "   Miss " + str(self.no_points)
            if self.value_progress_bar >= 99:
                self.count_points_win()

    def count_points_win(self):
        """ Called by count_point if value_progress_bar > 99 """
        # progress_bar.value = self.value_progress_bar
        self.get_time_2()
        if self.mode_game == "Colours Mode":
            self.get_time_final("Colours Mode")
        elif self.mode_game == "Text Mode":
            self.get_time_final("Text Mode")

        self.value_progress_bar = 0
        self.manager.current = 'win'
        BrainColorGame.sound_game.stop()
        BrainColorGame.sound_win.play()
        self.replay()

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
        name = self.colors_dict[name]
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
        if self.manager.current == 'menu' or \
                self.manager.current == 'game' or \
                self.manager.current == 'start':
            if keycode1 == 27 or keycode1 == 1001:
                self.replay()
                # Returning True will eat the keypress
                if self.manager.current == 'start':
                    MenuScreen.leave()
                if self.manager.current == 'menu':
                    self.manager.current = 'start'
                if self.manager.current == 'game':
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
            BrainColorGame.sound_game.volume = 0
        elif GameScreen.sound_pos == "mute":
            GameScreen.sound_pos = "unmute"
            BrainColorGame.sound_game.volume = 1


class WinScreen(Screen):
    """ On Win: Progress_bar """
    text1 = str(GameScreen.points)
    text2 = StringProperty("")
    text3 = StringProperty("")
    text4 = StringProperty("")
    text5 = StringProperty("")
    text6 = StringProperty("")

    @staticmethod
    def sound_stop():
        """ Game finish: change sound """
        BrainColorGame.sound_game.play()
        BrainColorGame.sound_win.stop()


class ButtonStart(ButtonBehavior, Image):
    """ Custom Button """
    def __init__(self, **kwargs):
        super(ButtonStart, self).__init__(**kwargs)
        # self.bind(state=self.state_changed)


class GameScreenRepeat(Screen):
    """ What do you want I describe here? ^^ """
    mode = 'forgot'  # forgot, remember
    easy_hard = 'easy'  # easy , hard
    question_index = 0
    bt1 = Button()
    bt2 = Button()
    bt3 = Button()
    bt4 = Button()
    colours = {'red': [1, 0, 0, 1],
               'blue': [0, 0, 1, 1],
               'yellow': [1, 1, 0, 1],
               'green': [0, 1, 0, 1]}
    colors = []
    question = []
    level = 2
    started = 0
    path = os.getcwd()
    bt1_sound = SoundLoader.load(path + '/bt1_sound.ogg')
    bt2_sound = SoundLoader.load(path + '/bt2_sound.ogg')
    bt3_sound = SoundLoader.load(path + '/bt3_sound.ogg')
    bt4_sound = SoundLoader.load(path + '/bt4_sound.ogg')
    sound_false = SoundLoader.load(path + '/sound_false.ogg')
    sound_win = SoundLoader.load(path + '/sound_win.ogg')

    def __init__(self, **kwargs):
        """ """
        super(GameScreenRepeat, self).__init__(**kwargs)
        self.ini()
        self.post_build_init()

    def post_build_init(self):
        """ Bind the android or the keyboard key """
        if platform() == 'android':
            import android
            android.map_key(android.KEYCODE_BACK, 1001)
        win = Window
        win.bind(on_keyboard=self.key_handler)

    def key_handler(self, window, keycode1, keycode2, text, modifiers):
        """ Called by escape key, 'reboot' the game """
        if self.manager.current == 'menu-repeat' or \
                self.manager.current == 'game-repeat':
            if keycode1 == 27 or keycode1 == 1001:
                if self.manager.current == 'menu-repeat':  # hum
                    BrainColorGame.sound_game.play()
                    self.manager.current = 'start'
                else:
                    self.level = 2
                    self.started = 0
                    self.question = []
                    self.colors = []
                    self.question_index = 0
                    self.manager.current = 'menu-repeat'
                return True
            return False

    def ini(self):
        """ build """
        self.level = 2
        self.question = []
        self.question_index = 0
        for num in range(self.level):
            self.question.append(random.choice(self.colours.values()))
            print len(self.question)

    def easy(self):
        """ See  MenuScreen Button in kv """
        self.easy_hard = 'easy'

    def hard(self):
        """ See  MenuScreen Button in kv """
        self.easy_hard = 'hard'

    def forgot(self):
        """ See  MenuScreen Button in kv """
        self.mode = 'forgot'

    def remember(self):
        """ See  MenuScreen Button in kv """
        self.mode = 'remember'

    def start(self, delta_time):
        """ Let's go """
        if self.manager.current == 'game-repeat':
            self.start_started(1)
        else:
            pass

    def start_started(self, delta_time):
        """ """
        BrainColorGame.sound_game.stop()
        bt1 = self.ids['bt1']
        bt2 = self.ids['bt2']
        bt3 = self.ids['bt3']
        bt4 = self.ids['bt4']
        print "here"
        print self.question_index
        print len(self.question)
        if bt1.background_color == self.colours['red'] and \
           bt2.background_color == self.colours['blue'] and \
           bt3.background_color == self.colours['yellow'] and \
           bt4.background_color == self.colours['green'] and \
           self.question_index < len(self.question):
            print "ok"
            if bt1.background_color == self.question[self.question_index]:
                bt1.background_color = [0.3, 1, 3, 1]
                self.bt1_sound.play()
                bt1.background_color = [0.3, 1, 3, 1]
            elif bt2.background_color == \
                    self.question[self.question_index]:
                bt2.background_color = [0.3, 1, 3, 1]
                self.bt2_sound.play()
            elif bt3.background_color == \
                    self.question[self.question_index]:
                bt3.background_color = [0.3, 1, 3, 1]
                self.bt3_sound.play()
            elif bt4.background_color == \
                    self.question[self.question_index]:
                bt4.background_color = [0.3, 1, 3, 1]
                self.bt4_sound.play()
            else:
                pass
            if self.easy_hard == 'easy':
                Clock.schedule_once(self.reboot_button, 1)
            elif self.easy_hard == 'hard':
                Clock.schedule_once(self.reboot_button, 0.5)

        else:
            pass

    def reboot_button(self, dt):
        """ Button have now the original color """
        bt1 = self.ids['bt1']
        bt2 = self.ids['bt2']
        bt3 = self.ids['bt3']
        bt4 = self.ids['bt4']

        print "reboot_button"
        self.question_index += 1
        bt1.background_color = self.colours['red']
        bt2.background_color = self.colours['blue']
        bt3.background_color = self.colours['yellow']
        bt4.background_color = self.colours['green']
        Clock.schedule_once(self.start, 0.3)

    def bt1_pressed(self):
        """ Check if the answer red is good """
        bt1 = self.ids['bt1']
        self.colors.append(bt1.background_color)
        print self.colors
        self.bt1_sound.play()
        self.check_answer()

    def bt2_pressed(self):
        """ Check if the answer blue is good """
        bt2 = self.ids['bt2']
        self.colors.append(bt2.background_color)
        print self.colors
        self.bt2_sound.play()
        self.check_answer()

    def bt3_pressed(self):
        """ Check if the answer yellow is good """
        bt3 = self.ids['bt3']
        self.colors.append(bt3.background_color)
        print self.colors
        self.bt3_sound.play()
        self.check_answer()

    def bt4_pressed(self):
        """ Check if the answer green is good """
        bt4 = self.ids['bt4']
        self.colors.append(bt4.background_color)
        print self.colors
        self.bt4_sound.play()
        self.check_answer()

    def win(self):
        """ Called by check_answer """
        self.sound_win.play()
        self.level += 1
        self.colors = []
        # Forgot the question or not
        if self.mode == 'forgot':
            self.question = []
            for x in range(self.level):
                self.question.append(random.choice(self.colours.values()))
        else:
                self.question.append(random.choice(self.colours.values()))

        print self.question
        self.question_index = 0
        Clock.schedule_once(self.start, 1)

    def check_answer(self):
        """ Called by Button's push """
        if self.colors == self.question:
            print "win"
            self.win()
        else:
            if len(self.colors) < len(self.question):
                for x in range(len(self.colors)):
                    print x
                    if self.colors[x] == self.question[x]:
                        print "ok"
                    else:
                        print "false"
                        self.colors = []
                        self.question_index = 0
                        Clock.schedule_once(self.start, 0.5)
                        print "Question: " + str(self.question)
                        self.sound_false.play()
            else:
                print "you loose"
                self.sound_false.play()
                self.colors = []
                print "Question: " + str(self.question)
                self.question_index = 0
                Clock.schedule_once(self.start, 0.5)


class MenuScreenRepeat(Screen):
    """ The Menu Class """
    text_easiest = "Easiest"
    text_easy = "Medium"
    text_medium = "Hard"
    text_hard = "Hard"

    @staticmethod
    def leave():
        """ Good by! """
        App.get_running_app().stop()

    @staticmethod
    def start_game():
        """ Ok let's play ! """
        Screen.manager.current = 'game-repeat'


class BrainColorGame(App):
    """ Main App """
    sound_game = SoundLoader.load('BCG-01.ogg')
    sound_game.loop = True
    sound_win = SoundLoader.load("win.ogg")

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

    def build_config(self, config):
        """ Not use, maybe should display best scorses """
        config.setdefaults('section',
                           {
                               'key1': '43',
                               'key2': '45'
                           })

    def build_settings(self, settings):
        """ Open the json settings """
        with open("settings.json", "r") as settings_json:
            settings.add_json_panel('Brain Color Game',
                                    self.config,
                                    data=settings_json.read())

    def build(self):
        """ Use ScreenManager """
        self.use_kivy_settings = False
        self.settings_cls = SettingsWithNoMenu
        self.sound_game.play()
        self.bind(text_2=self.update)
        # Create the screen manager
        screen_m = ScreenManager()
        screen_m = ScreenManager(transition=FadeTransition())
        screen_m.add_widget(StartScreen(name='start'))
        screen_m.add_widget(MenuScreen(name='menu'))
        screen_m.add_widget(GameScreen(name='game'))
        screen_m.add_widget(GameScreenRepeat(name='game-repeat'))
        screen_m.add_widget(MenuScreenRepeat(name='menu-repeat'))
        screen_m.add_widget(WinScreen(name='win'))
        return screen_m

    def update(self, *args):
        """ build self.bind """

    def on_pause(self):
        """ Enable pause on mobile """
        self.sound_game.volume = 0
        return True

    def on_resume(self):
        self.sound_game.volume = 1


if __name__ == '__main__':
    BrainColorGame().run()
