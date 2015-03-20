from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')

import kivy
kivy.require('1.0.8')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    player1Dir = 0
    player2Dir = 0

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[0] == 273:
            self.player1Dir = 0
        elif keycode[0] == 274:
            self.player1Dir = 0;

        if keycode[0] == 114:
            self.player2Dir = 0
        elif keycode[0] == 102:
            self.player2Dir = 0;


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # 273 up
        # 274 down
        # 275 right
        # 276 left
        # 308 ALT
        # 306 CTRL

        # 114 r
        # 102 f
        # 103 g
        # 100 d
        #  97 a
        # 115 s

        if keycode[0] == 273:
            self.player1Dir = 1
        elif keycode[0] == 274:
            self.player1Dir = -1;

        if keycode[0] == 114:
            self.player2Dir = 1
        elif keycode[0] == 102:
            self.player2Dir = -1


        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        player1Offset = self.player1Dir * 5
        self.player1.center_y += player1Offset

        player2Offset = self.player2Dir * 5
        self.player2.center_y += player2Offset

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        #went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            print touch.y
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
