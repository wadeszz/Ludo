# Полноценная Ludo-игра — будет заполняться в следующих шагах
# Это базовый шаблон main.py с подготовленной структурой

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from kivy.animation import Animation
import random

class Token(Widget):
    def __init__(self, color, team, index, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.team = team
        self.index = index
        self.size = (40, 40)
        self.steps = 0
        with self.canvas:
            Color(*self.color)
            self.circle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics)

    def update_graphics(self, *args):
        self.circle.pos = self.pos

class LudoBoard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tokens = []
        self.positions = self.generate_path()
        self.init_tokens()

    def generate_path(self):
        # Простейший путь из 72 позиций (по кругу)
        path = []
        for i in range(72):
            x = 100 + (i % 12) * 35
            y = 400 - (i // 12) * 35
            path.append((x, y))
        return path

    def init_tokens(self):
        colors = [(1, 0, 0), (0, 1, 0), (0, 0.6, 1), (1, 1, 0)]
        for team in range(4):
            for i in range(4):
                t = Token(color=colors[team], team=team, index=i)
                t.pos = (50 + team * 100, 50 + i * 50)
                self.tokens.append(t)
                self.add_widget(t)

    def move_token(self, token, steps):
        token.steps += steps
        if token.steps >= len(self.positions):
            token.steps = len(self.positions) - 1
        new_pos = self.positions[token.steps]
        Animation(pos=new_pos, duration=0.3 * steps).start(token)

class GameUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.board = LudoBoard(size_hint=(1, 0.75))
        self.roll_label = Label(text="🎲 Готов к броску", font_size=32, size_hint=(1, 0.1))
        self.roll_button = Button(text="Бросить кубик", font_size=30, size_hint=(1, 0.15))
        self.roll_button.bind(on_press=self.roll_dice)
        self.add_widget(self.board)
        self.add_widget(self.roll_label)
        self.add_widget(self.roll_button)
        self.current_player = 0
        self.rolled = 0

    def roll_dice(self, instance):
        self.rolled = random.randint(1, 6)
        self.roll_label.text = f"🎲 Выпало: {self.rolled}"
        Clock.schedule_once(self.auto_move, 1)

    def auto_move(self, dt):
        # Простейшая логика: двигаем первую доступную фишку игрока
        team_tokens = [t for t in self.board.tokens if t.team == self.current_player]
        token = team_tokens[0]
        self.board.move_token(token, self.rolled)

        # Передача хода (если не 6)
        if self.rolled != 6:
            self.current_player = (self.current_player + 1) % 4

class LudoApp(App):
    def build(self):
        return GameUI()

if __name__ == "__main__":
    LudoApp().run()