from mydevoirs.widgets import CarouselWidget
from kivy.app import App
from kivy.properties import ObjectProperty
from mydevoirs.constants import APP_NAME
from pathlib import Path
from mydevoirs.utils import get_dir
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.modules import inspector

from mydevoirs.database.database import db_init

from mydevoirs.settings import settings_json
from mydevoirs.slide_item import SettingSlider


class Agenda(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carousel = CarouselWidget()
        self.add_widget(self.carousel)

    def go_date(self, date=None):
        self.remove_widget(self.carousel)

        self.carousel = CarouselWidget(date)

        self.add_widget(self.carousel)


class MyDevoirsApp(App):

    carousel = ObjectProperty()

    def __init__(self):
        db_init()
        super().__init__()

        assert self.get_application_name() == APP_NAME

    def build(self):
        self.sm = ScreenManager(transition=SlideTransition(direction="up"))
        agenda = Agenda(name="agenda")
        todo = Screen(name="todo")
        self.sm.add_widget(agenda)
        self.sm.add_widget(todo)
        self.sm.current = "agenda"

        self.box = BoxLayout(orientation="vertical")
        self.box.add_widget(ActionBar())
        self.box.add_widget(self.sm)
        inspector.create_inspector(Window, self.sm)
        print(self.sm.ids)

        return self.box

    def go_todo(self):
        self.sm.current = "todo"

    def go_agenda(self):
        self.sm.current = "agenda"
        self.sm.current_screen.go_date()

    def build_config(self, config):
        config.setdefaults(
            "agenda",
            {
                "lundi": True,
                "mardi": True,
                "mercredi": False,
                "jeudi": True,
                "vendredi": True,
                "samedi": False,
                "dimanche": False,
            },
        )

    def build_settings(self, settings):
        settings.add_json_panel("agenda", self.config, data=settings_json)

    def on_config_change(self, config, *args):
        self.go_date()

    def get_application_config(self):
        return super().get_application_config(
            Path(get_dir("config"), "settings.ini").absolute()
        )
