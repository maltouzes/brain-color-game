# -*- coding: utf-8 -*-
""" A simple Color Game make with kivy """
__version__ = '0.2.22'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.popup import Popup
# from kivy.core.window import Window
from plyer import vibrator

import random
# import platform
import time


class BoxLayoutGame(BoxLayout):
    """ BoxLayout called by kivy """
    sound = SoundLoader.load('Single_Ply_Prison_Mastered.ogg')
    sound.loop = True
    sound.play()
    sound_win = SoundLoader.load("win.ogg")
    sound_pos = "unmute"
# Text when the game start
    text = 'Push a button for start'
    value_progress_bar = 0
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
    popup_open = "False"

# Choose the game mode, by default: Colours Mode
    mode_game = ""
    old_mode_game = ""
    _popup = ObjectProperty(None)
# Time
    time_1 = ""
    time_2 = 0
    t_final = ""
    t_best = 100.
    records = "New Records = "
    time_mode = 0

    def change_time_mode(self):
        """ Enable or Disable time_mode """
        if self.time_mode == 0:
            self.time_mode = 1
        else:
            self.time_mode = 0
        print self.time_mode

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

    # def __init__(self, **kwargs):
        # super(BoxLayoutGame, self).__init__(**kwargs)
        # self._keyboard = Window.request_keyboard(
            # self._keyboard_closed, self, 'text')
        # if self._keyboard.widget:
        # If it exists, this widget is a VKeyboard object which you can use
        # to change the keyboard layout.
        # pass
        # self._keyboard.bind(on_key_down=self._on_keyboard_down)

    # def _keyboard_closed(self):
        # """ Close the keyboard """
        # print'My keyboard have been closed!'
        # self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        # self._keyboard = None

    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # """ call leave_popup or popup_open """
        # print 'The key', keycode, 'have been pressed'
        # print ' - text is %r' % text
        # print ' - modifiers are %r' % modifiers

        # if keycode[1] == 'escape':
            # keyboard.release()
        # if keycode[1] == 'a':
        # if self.popup_open == "True":
            # print self.popup_open
            # print "Leave apps?"
            # self.show_leave_popup()
            # App.get_running_app().stop()
            # else:
            # self.show_popup(1)
            # self.sound_play()
            # print self.popup_open
        # if keycode[1] == 'android.KEYCODE_BACK':
            # if self.popup_open == "True":
            # print self.popup_open
            # print "Leave apps?"
            # self.show_leave_popup()
            # App.get_running_app().stop()
            # else:
            # self.show_popup(1)
            # self.sound_play()
            # print self.popup_open

        # return True

    def on_pause(self):
        """ Enable pause on mobile """
        return True

    @staticmethod
    def leave():
        """ Leave the apps """
        App.get_running_app().stop()

    def popup_open_change(self):
        """ on_keyboard_don """
        self.popup_open = "False"
        print self.popup_open

    def show_popup(self, dtime):
        """ Welcome popup  """
        PopupWelcome.text = "Please choose a mode"
        content = PopupWelcome(cancel=self.dismiss_popup,
                               start_text_mode=self.start_text_mode,
                               start_color_mode=self.start_color_mode,
                               sound_validation=self.sound_validation,
                               popup_open_change=self.popup_open_change,
                               reboot_progress_bar=self.reboot_progress_bar,
                               sound_play=self.sound_play,
                               change_time_mode=self.change_time_mode)
        self._popup = Popup(title="Brain Color Game",
                            title_align='center',
                            title_color=[1, 1, 0, 1],
                            title_size=20,
                            separator_color=[1, 1, 0, 1],
                            separator_height=5,
                            content=content,
                            size_hint=(1, 1))
        self.popup_open = "True"
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
        BoxLayoutGame.mode_game = "Text Mode"
        print BoxLayoutGame.mode_game
        self.restart()

    def start_color_mode(self):
        """ show_popup: start Colours Mode """
        BoxLayoutGame.mode_game = "Colours Mode"
        print BoxLayoutGame.mode_game
        self.restart()

    def show_leave_popup(self):
        """ show LeavePopup """
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

    def go_start(self):
        """ Show show_popup when the apps start """
        Clock.schedule_once(self.show_popup, 0)

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
        self.points_kv = self.ids['points']
        progress_bar = self.ids['progress']
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
                    self.points += 1
                    self.value_progress_bar += 3
                    self.sound_points_play()
                else:
                    self.no_points += 1
                    try:
                        vibrator.vibrate(0.4)
                    except NotImplementedError:
                        pass
                    BoxLayoutGame.sound_miss_play()
                self.points_kv.text = "Points " + str(self.points) +\
                                      "   Miss " + str(self.no_points)
                progress_bar.value = self.value_progress_bar
            elif self.mode_game == "Text Mode":
                # Text Mode
                if nbr == self.number_random:
                    self.points += 1
                    self.value_progress_bar += 3
                    self.sound_points_play()
                else:
                    self.no_points += 1
                    try:
                        vibrator.vibrate(0.4)
                    except NotImplementedError:
                        pass

                    BoxLayoutGame.sound_miss_play()
                self.points_kv.text = "Points " + str(self.points) +\
                                      "   Miss " + str(self.no_points)
                progress_bar.value = self.value_progress_bar
            else:
                pass
            if self.value_progress_bar >= 50:
                progress_bar.value = self.value_progress_bar
                self.get_time_2()
                self.get_time_final()
                self.progress_bar_chalenge()
            else:
                pass

    def restart(self):
        """ Restart the game in another mode  """
        # mode_game_kv = self.ids['spinner_game']
        self.points_kv = self.ids['points']
        # if mode_game_kv.text != self.mode_game:
        if self.mode_game != self.old_mode_game:
            self.points = 0
            self.no_points = 0
            self.points_kv.text = ""
            self.ask()
        # self.points_kv.text = "Push a button for start"
            # if self.mode_game == "Colours Mode":
            # self.text = "Start Colours Mode"
            # self.points_str = ""
            # self.points_kv.text = "Push on the good text"
            # elif self.mode_game == "Text Mode":
            # self.text = "Start Text Mode"
            # self.points_str = ""
            # self.points_kv.text = "Push on the Good Color"
            # else:
            # pass
            self.old_mode_game = self.mode_game
            self.time_1 = ""
        else:
            pass

    def replay(self):
        """ Button replay """
        progress_bar = self.ids['progress']
        self.value_progress_bar = 0
        progress_bar.value = self.value_progress_bar
        self.points_kv = self.ids['points']
        self.points = 0
        self.no_points = 0
        self.points_kv.text = ""
        self.ask()
        self.time_1 = ""
        self.sound_win.stop()
        self.sound.play()

    def reboot_progress_bar(self):
        """ reboot the progress bar """
        progress_bar = self.ids['progress']
        self.value_progress_bar = 0
        progress_bar.value = self.value_progress_bar

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

    @staticmethod
    def sound_validation():
        """ Play a sound when call by MyButton: kv file """
        sound_valid = SoundLoader.load("validation.ogg")
        sound_valid.play()

    def spinner_restart(self):
        """ Restart all text when click on spinner """
        # welcome = self.ids['welcome_text']
        # welcome.text = "Please push a button for start"
        # points_kv = self.ids['points']
        # self.points_str = ""
        # points_kv.text = self.points_str
        # self.no_points = 0
        # self.points = 0
        self.sound.stop()
        self.sound.play()

    def self_active(self):
        """ Used by CheckBox: mute or unmute music """
        if self.sound_pos == "mute":
            self.sound.volume = 1
            self.sound_pos = "unmute"
        elif self.sound_pos == "unmute":
            self.sound_pos = "mute"
            self.sound.volume = 0


class MyButton(Button):
    """ Custom Spinner Button """
    # @staticmethod
    # def sound():
    # """ Play a sound when call by MyButton: kv file """
    # sound_valid = SoundLoader.load("validation.ogg")
    # sound_valid.play()


class MySpinner(Spinner):
    """ Custom Spinner """
    option_cls = ObjectProperty(MyButton)
    values = ListProperty()


class PopupWelcome(BoxLayout):
    """ Popup open when start the app """
    cancel = ObjectProperty(None)
    start_text_mode = ObjectProperty(None)
    start_color_mode = ObjectProperty(None)
    sound_validation = ObjectProperty(None)
    popup_open_change = ObjectProperty(None)
    reboot_progress_bar = ObjectProperty(None)
    sound_play = ObjectProperty(None)
    change_time_mode = ObjectProperty(None)


class LeavePopup(BoxLayout):
    """ Leave the apps """
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
        BoxLayoutGame().go_start()
        return BoxLayoutGame()


if __name__ == '__main__':
    ColorAndTextApp().run()
