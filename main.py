# -*- coding: utf-8 -*-
""" A simple Color Game made with kivy """
__version__ = '0.2.32'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.core.window import Window
from plyer import vibrator
from kivy.utils import platform

import random
import time


class BoxLayoutGame(BoxLayout):
    """ BoxLayout called by kivy """
    _popup = ObjectProperty(None)
    # Music during the game
    sound = SoundLoader.load('BCG-01.ogg')
    sound.loop = True
    sound.play()
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
    points = 0
    no_points = 0
    # start the game
    points_str = " "

    # Choose the game mode, by default: Colours Mode
    mode_game = ""
    old_mode_game = ""
    # Time
    time_1 = ""
    time_2 = 0
    # time_2 - time1
    t_final = ""
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
        super(BoxLayoutGame, self).__init__(**kwargs)
        # From kivy.utils source code: freebsd = linux, darwin = macosx
        if platform == 'linux' or platform == 'win' or platform == 'macosx':
            # Display menu on screen if platform == Desktop
            box = BoxLayout(spacing=5,
                            padding=[5, 5, 5, 5],
                            size_hint_y=None)
            btn2 = Button(text='Menu',
                          background_color=[0.3, 0.06, 0.23, 1],
                          size_hint_y=None)
            btn1 = Button(text='Restart',
                          background_color=[0.3, 0.06, 0.23, 1],
                          size_hint_y=None)
            btn2.bind(on_press=lambda a: self.go_start())
            btn2.bind(on_press=lambda a: self.sound_play())
            btn1.bind(on_press=lambda a: self.replay())
            box.add_widget(btn2)
            box.add_widget(btn1)
            self.add_widget(box)
        self.go_start()
        self.post_build_init()

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
            self.go_start()
        # Returning True will eat the keypress
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
            self.replay()
        else:
            self.time_mode = 0
            self.active = False
            self.remove_widget(self.progress_bar_1)

    def get_time_1(self):
        """ Used for start chronometer  """
        self.time_1 = time.time()

    def get_time_2(self):
        """ Used for end chronometer """
        self.time_2 = time.time()

    def get_time_final(self):
        """ chronometer time """
        self.t_final = self.time_2 - self.time_1
        self.t_final = "%.2f" % self.t_final
        if float(self.t_final) < float(self.t_best):
            self.t_best = self.t_final
            self.records = "New Records = "
            self.sound_win.play()
            self.sound.stop()
        else:
            self.records = "Best Records = "
            self.sound_validation()

    @staticmethod
    def leave():
        """ Leave the apps """
        App.get_running_app().stop()

    def go_start(self):
        """ Show show_popup when the apps start """
        Clock.schedule_once(self.show_popup, 0)

    def show_popup(self, dtime):
        """ Welcome popup """
        content = PopupWelcome(cancel=self.dismiss_popup,
                               start_text_mode=self.start_text_mode,
                               start_color_mode=self.start_color_mode,
                               sound_validation=self.sound_validation,
                               reboot_progress_bar=self.reboot_progress_bar,
                               sound_play=self.sound_play,
                               change_time_mode=self.change_time_mode,
                               leave=self.leave)
        self._popup = Popup(title="Brain Color Game",
                            title_align='center',
                            title_color=[1, 1, 0, 1],
                            title_size=20,
                            separator_color=[1, 1, 0, 1],
                            separator_height=5,
                            content=content,
                            size_hint=(1, 1))
        self._popup.open()

    def progress_bar_chalenge(self):
        """ Popup """
        XBoxLayout.text = "You win "
        XBoxLayout.text2 = str(self.t_final) + " seconds"
        XBoxLayout.text3 = self.records + str(self.t_best)
        content = XBoxLayout(cancel=self.dismiss_popup,
                             replay=self.replay,
                             reboot_progress_bar=self.reboot_progress_bar)
        self._popup = Popup(title="You win !!!",
                            content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def start_text_mode(self):
        """ show_popup: start Text Mode """
        self.mode_game = "Text Mode"
        self.restart()

    def start_color_mode(self):
        """ show_popup: start Colours Mode """
        self.mode_game = "Colours Mode"
        self.restart()

    def show_leave_popup(self):
        """ show LeavePopup """
        # NOT USED
        LeavePopup.text = "Do you want to leave?"
        content = LeavePopup(cancel=self.dismiss_popup,
                             leave=self.leave)
        self._popup = Popup(title="Brain Color Game",
                            title_color=[0, 1, 0, 1],
                            content=content,
                            size_hint=(1, 1))
        self._popup.open()

    def dismiss_popup(self):
        """ Used for dismiss_PopupWelcome """
        self._popup.dismiss()

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
        # self.restart()
        welcome.text = self.text

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
                    self.points += 50
                    if self.active is True:
                        # time mode active
                        self.value_progress_bar += 3
                    else:
                        pass
                    self.sound_points_play()
                else:
                    # Miss
                    self.no_points += 1
                    # On Android
                    try:
                        vibrator.vibrate(0.4)
                    except NotImplementedError:
                        pass
                    BoxLayoutGame.sound_miss_play()
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
                    BoxLayoutGame.sound_miss_play()
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
                self.progress_bar_chalenge()
            else:
                pass

    def restart(self):
        """ Restart the game in another mode  """
        points_kv = self.ids['points']
        # if mode_game_kv.text != self.mode_game:
        # if self.mode_game != self.old_mode_game:
        self.points = 0
        self.no_points = 0
        points_kv.text = ""
        self.ask()
        self.old_mode_game = self.mode_game
        self.time_1 = ""

    def replay(self):
        """ Button replay """
        self.value_progress_bar = 0
        try:
            self.progress_bar_1.value = self.value_progress_bar
        except AttributeError:
            pass
        points_kv = self.ids['points']
        self.points = 0
        self.no_points = 0
        points_kv.text = ""
        self.ask()
        self.time_1 = ""
        self.sound_win.stop()
        self.sound.play()

    def reboot_progress_bar(self):
        """ reboot the progress bar """
        self.value_progress_bar = 0
        try:
            self.progress_bar_1.value = self.value_progress_bar
        except AttributeError:
            pass

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

    def self_active(self):
        """ Used by CheckBox: mute or unmute music """
        if self.sound_pos == "mute":
            self.sound.volume = 1
            self.sound_pos = "unmute"
        elif self.sound_pos == "unmute":
            self.sound_pos = "mute"
            self.sound.volume = 0


class PopupWelcome(BoxLayout):
    """ Popup open when start the app """
    cancel = ObjectProperty(None)
    start_text_mode = ObjectProperty(None)
    start_color_mode = ObjectProperty(None)
    sound_validation = ObjectProperty(None)
    reboot_progress_bar = ObjectProperty(None)
    sound_play = ObjectProperty(None)
    change_time_mode = ObjectProperty(None)
    leave = ObjectProperty(None)


class LeavePopup(BoxLayout):
    """ Leave the apps """
    # NOT USED
    cancel = ObjectProperty(None)
    leave = ObjectProperty(None)


class XBoxLayout(BoxLayout):
    """ Default BoxLayout """
    cancel = ObjectProperty(None)
    replay = ObjectProperty(None)
    reboot_progress_bar = ObjectProperty(None)


class ColorAndTextApp(App):
    """ Kivy App """
    def build(self):
        """ Build the App """
        return BoxLayoutGame()

if __name__ == '__main__':
    PROG = ColorAndTextApp()
    PROG.run()
