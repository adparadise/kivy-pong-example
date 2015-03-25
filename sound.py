#!/usr/bin/python

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')

import kivy
import math
kivy.require('1.0.8')
from kivy.properties import BooleanProperty
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import *
from kivy.core.audio import SoundLoader
import io
from kivy.core.image import Image as CoreImage

class SoundGame(Widget):
    isPlaying = False
    isPlayingRequested = False
    index = 0
    filename = "daft-punk.wav"
    sound = None

    def __init__(self, **kwargs):
        super(SoundGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.sound = SoundLoader.load(self.filename)
        self.sound.loop = True
        self.color = Color(0.3, 0.5, 0.6)

        data = io.BytesIO(open("plums.tiff", "rb").read())
        im = CoreImage(data, ext="png")
        self.rect = Rectangle(texture=im.texture, pos=(40, 25), size=(100, 100))

        self.canvas.add(self.color)
        self.canvas.add(self.rect)

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[0] == 114:
            self.isPlayingRequested = False


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 114:
            self.isPlayingRequested = True

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def update(self, dt):
        isChanged = False
        if not self.isPlaying and self.isPlayingRequested:
            self.isPlaying = True
            isChanged = True
        elif self.isPlaying and not self.isPlayingRequested:
            self.isPlaying = False
            isChanged = True

        self.index += 1
        cos = math.cos(self.index * math.pi / 360)
        sin = math.sin(self.index * math.pi / 360)
        self.rect.pos = (cos * 100 + 90, sin * 100 + 75)
        size = 32
        width = 800.0
        height = 608.0
        x = 11
        y = 2
        u = x * size / width
        v = y * size / height
        w = size / width
        h = size / height
        self.rect.tex_coords = [u, v + h, u + w, v + h, u + w, v, u, v]

        if isChanged:
            if self.isPlaying:
                self.color.r = 0.6
                self.color.b = 0.3
            else:
                self.color.r = 0.3
                self.color.b = 0.6

        if isChanged:
            if self.isPlaying:
                self.sound.play()
            else:
                self.sound.stop()

class SoundApp(App):
    def build(self):
        game = SoundGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    SoundApp().run()
