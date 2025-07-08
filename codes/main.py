import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard
from kivy.graphics import Color, RoundedRectangle

Window.size = (360, 640) 
Window.clearcolor = (0.1, 0.1, 0.1, 1) 

class PasswordGameApp(App):
    icon = 'icon.png'
    def build(self):
        self.rules = self.get_all_rules()
        random.shuffle(self.rules)
        self.passed_rules = set()
        self.rule_widgets = []
        self.active_rule = None
        self.first_input_done = False

        self.layout = FloatLayout()

        self.fail_sounds = [
            SoundLoader.load("sounds/fail.wav"),
            SoundLoader.load("sounds/fail2.wav"),
            SoundLoader.load("sounds/fail3.wav"),
            SoundLoader.load("sounds/fail4.wav")
        ]

        self.title_label = Label(
            text="[b]ENTER YOUR\nPASSWORD[/b]",
            markup=True,
            font_size=35,
            font_name="fonts/habeshapixels.bold.ttf",
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={'center_x': 0.5, 'top': 0.92},
            halign='center'
        )

        self.password_input = TextInput(
            password=False,
            multiline=False,
            font_size=22,
            font_name="fonts/habeshapixels.regular.ttf",
            size_hint=(0.65, None),
            height=55,
            pos_hint={'center_x': 0.5, 'top': 0.78},
            background_normal='',
            background_active='',
            background_color=(0.3, 0.3, 0.3, 1), 
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 0.6, 0.1, 1),
            padding=(15, 12),
            halign='center'
        )

        self.submit_btn = Button(
            text="SUBMIT",
            font_size=23,
            font_name="fonts/habeshapixels.bold.ttf",
            color=(0, 0, 0, 1),
            size_hint=(0.35, None),
            height=50,
            pos_hint={'center_x': 0.5, 'y': 0.05},
            background_normal='',
            background_down='',
            background_color=(1, 0.5, 0.1, 1) 
        )
        self.submit_btn.bind(on_press=self.check_password)

        self.result_label = Label(
            text="",
            font_size=20,
            font_name="fonts/habeshapixels.regular.ttf",
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(600, 40),
            pos_hint={'center_x': 0.5, 'top': 0.86}
        )

        self.rules_container = FloatLayout()

        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(self.submit_btn)
        self.layout.add_widget(self.rules_container)
        self.layout.add_widget(self.password_input)

        return self.layout

    def get_all_rules(self):
        return [
            {"message": "Must be at least 10 characters", "check": lambda p: len(p) >= 10},
            {"message": "Must include a number", "check": lambda p: any(c.isdigit() for c in p)},
            {"message": "Must include '@' or '#'", "check": lambda p: '@' in p or '#' in p},
            {"message": "Must start with a capital letter", "check": lambda p: p and p[0].isupper()},
            {"message": "Must include the word 'cat'", "check": lambda p: 'cat' in p.lower()},
            {"message": "Must include a special symbol (!@#$%^&*)", "check": lambda p: any(c in '!@#$%^&*' for c in p)},
            {"message": "Must include both upper and lower case letters", "check": lambda p: any(c.islower() for c in p) and any(c.isupper() for c in p)},
            {"message": "Must end with a digit", "check": lambda p: p[-1].isdigit() if p else False},
            {"message": "Must include at least 3 vowels", "check": lambda p: sum(p.lower().count(v) for v in 'aeiou') >= 3},
            {"message": "Must not contain spaces", "check": lambda p: ' ' not in p},
            {"message": "Must contain '123' in sequence", "check": lambda p: '123' in p},
            {"message": "Must include a month name", "check": lambda p: any(m in p.lower() for m in ['january','february','march','april','may','june','july','august','september','october','november','december'])},
            {"message": "Must include a year (e.g. 2023)", "check": lambda p: any(str(y) in p for y in range(1990, 2031))},
            {"message": "Must contain a palindrome like 'aba'", "check": lambda p: any(p[i:i+3] == p[i:i+3][::-1] for i in range(len(p)-2))},
            {"message": "Must not contain 'password'", "check": lambda p: 'password' not in p.lower()},
            {"message": "Must contain a dot '.'", "check": lambda p: '.' in p},
            {"message": "Must include 'qwe' keyboard pattern", "check": lambda p: 'qwe' in p.lower()},
            {"message": "Must contain the letter 'z'", "check": lambda p: 'z' in p.lower()},
            {"message": "Must contain a hyphen '-'", "check": lambda p: '-' in p},
            {"message": "Must contain a word from tech: 'ai', 'bot', 'ml'", "check": lambda p: any(w in p.lower() for w in ['ai', 'bot', 'ml'])},
        ]

    def check_password(self, instance):
        pwd = self.password_input.text.strip().lower()

        if pwd == "rickroll":
            self.show_rickroll_popup()
            return

        if pwd == "pig":
            self.spawn_bouncing_emoji("🐷")
            return

        if pwd == "i give up":
            self.show_popup(pwd)
            return

        if random.random() < 0.05:
            sound = random.choice(self.fail_sounds)
            if sound:
                sound.play()

        if random.random() < 0.5:
            anim = Animation(pos_hint={
                'center_x': random.uniform(0.2, 0.8),
                'y': random.uniform(0.1, 0.6)
            }, duration=0.3)
            anim.start(self.submit_btn)

        if not self.first_input_done:
            self.first_input_done = True
            self.show_next_rule()
            return

        if self.active_rule and self.active_rule['check'](self.password_input.text):
            self.passed_rules.add(self.active_rule['message'])
            self.result_label.text = ""
            self.show_next_rule()
        else:
            self.shake_input()


    def show_next_rule(self):
        pwd = self.password_input.text
        for rule in self.rules:
            if rule['message'] in self.passed_rules:
                continue
            if rule['check'](pwd):
                self.passed_rules.add(rule['message'])
                continue
            self.active_rule = rule
            box = self.create_rule_box(rule['message'])
            self.rules_container.add_widget(box)
            self.rule_widgets.insert(0, box)
            self.animate_rule_positions()
            return

        self.show_popup(pwd)

    def create_rule_box(self, message):
        box = BoxLayout(orientation='vertical',
                        size_hint=(0.6, None),
                        height=50,
                        pos_hint={'center_x': 0.5, 'top': 0.7})
        
        with box.canvas.before:
            Color(0.2, 0.2, 0.2, 0.8) 
            box.bg = RoundedRectangle(radius=[10], pos=box.pos, size=box.size)

        box.bind(pos=self.update_box_bg, size=self.update_box_bg)

        label = Label(
            text=f"[b]{message}[/b]",
            markup=True,
            font_size=16,
            font_name="fonts/habeshapixels.bold.ttf",
            color=(1, 0.8, 0.3, 1),
            halign="center",
            valign="middle"
        )
        label.bind(size=label.setter("text_size"))
        box.add_widget(label)
        return box

    def update_box_bg(self, instance, *args):
        instance.bg.pos = instance.pos
        instance.bg.size = instance.size


    def animate_rule_positions(self):
        for i, widget in enumerate(self.rule_widgets):
            target_top = 0.7 - i * 0.08
            target_opacity = max(0.3, 1.0 - i * 0.15)
            Animation(pos_hint={'center_x': 0.5, 'top': target_top}, opacity=target_opacity, duration=0.4).start(widget)
        if len(self.rule_widgets) > 6:
            to_remove = self.rule_widgets.pop()
            self.rules_container.remove_widget(to_remove)

    def show_popup(self, pwd):
        layout = BoxLayout(orientation='vertical', spacing=12, padding=20)
        layout.opacity = 0

        label = Label(
            text=f"[b]\nCONGRATS! You created a strong password:[/b]\n[color=ffdd44]{pwd}[/color]",
            markup=True,
            font_size=25,
            font_name="fonts/habeshapixels.regular.ttf",
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=160
        )

        label.bind(size=label.setter("text_size"))
        
        try_again_btn = Button(
            text="Try Again",
            font_name="fonts/habeshapixels.bold.ttf",
            size_hint_y=None,
            height=40,
            on_press=self.reset_game
        )
        share_btn = Button(
            text="Share",
            font_name="fonts/habeshapixels.bold.ttf",
            size_hint_y=None,
            height=40,
            on_press=lambda x: self.copy_to_clipboard(pwd)
        )

        layout.add_widget(label)
        layout.add_widget(try_again_btn)
        layout.add_widget(share_btn)

        self.popup = Popup(title="", title_align='center', content=layout,
                           size_hint=(0.85, None), height=320, auto_dismiss=True)
        self.popup.open()
        Animation(opacity=1, duration=0.3).start(layout)

    def reset_game(self, popup):
        self.password_input.text = ""
        self.result_label.text = ""
        self.rules_container.clear_widgets()
        self.rule_widgets.clear()
        self.passed_rules.clear()
        self.first_input_done = False
        self.active_rule = None
        self.submit_btn.pos_hint = {'center_x': 0.5, 'y': 0.05}
        if hasattr(self, 'popup'):
            self.popup.dismiss()

    def copy_to_clipboard(self, pwd):
        Clipboard.copy(pwd)
        self.result_label.text = "Password copied to clipboard!"

    def shake_input(self):
        anim = (
            Animation(x=self.password_input.x - 10, duration=0.05) +
            Animation(x=self.password_input.x + 10, duration=0.05) +
            Animation(x=self.password_input.x - 8, duration=0.05) +
            Animation(x=self.password_input.x + 8, duration=0.05) +
            Animation(x=self.password_input.x, duration=0.05)
        )
        anim.start(self.password_input)

    def show_rickroll_popup(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        label = Label(
            text="[b][color=ff5555] Never gonna give you up![/color][/b]",
            markup=True,
            font_size=24,
            font_name="fonts/habeshapixels.regular.ttf",
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter("text_size"))

        close_btn = Button(
            text="Close",
            font_name="fonts/habeshapixels.bold.ttf",
            size_hint_y=None,
            height=40,
            on_press=lambda x: self.rickroll_popup.dismiss()
        )

        layout.add_widget(label)
        layout.add_widget(close_btn)

        self.rickroll_popup = Popup(title="", content=layout, size_hint=(0.8, None), height=200)
        self.rickroll_popup.open()

    def spawn_bouncing_emoji(self, emoji_char):
        emoji_label = Label(
            text=emoji_char,
            font_size=64,
            size_hint=(None, None),
            size=(100, 100),
            pos=(random.randint(0, 260), random.randint(0, 540)) 
        )
        self.layout.add_widget(emoji_label)

        self.bounce_emoji(emoji_label, dx=5, dy=5)
    def bounce_emoji(self, widget, dx, dy):
        def move(dt):
            new_x = widget.x + dx
            new_y = widget.y + dy

            if new_x < 0 or new_x + widget.width > Window.width:
                dx_ref[0] *= -1
            if new_y < 0 or new_y + widget.height > Window.height:
                dy_ref[0] *= -1

            widget.x += dx_ref[0]
            widget.y += dy_ref[0]

        from kivy.clock import Clock
        dx_ref = [dx]
        dy_ref = [dy]
        Clock.schedule_interval(move, 1/60)



if __name__ == '__main__':
    PasswordGameApp().run()
