import platform
import subprocess
import sys
from configparser import ConfigParser
from pathlib import Path

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from pony.orm import OperationalError

import mydevoirs.database
from mydevoirs.constants import BASE_DIR
from mydevoirs.custom_setting import (
    SettingCustomConfigFilePath,
    SettingFilePath,
    SettingLabel,
)
from mydevoirs.database import init_database
from mydevoirs.settings import DEFAULT_SETTINGS, SETTING_PANELS
from mydevoirs.utils import get_dir, get_matiere_color
import logging

LOG = logging.getLogger(__name__)


class MyDevoirsApp(App):

    use_kivy_settings = False

    carousel = ObjectProperty()

    title = "MyDevoirs"

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def init_database(self):
        path = self.load_config()["ddb"]["path"]
        try:
            mydevoirs.database.db = init_database(filename=path, create_db=True)
        except OperationalError as err:
            LOG.error("Echec de création de la base de donnée")
            raise err

    def build(self):
        from mydevoirs.agenda import Agenda
        from mydevoirs.colorchooser import ColorChooser
        from mydevoirs.todo import Todo

        self.sm = ScreenManager(transition=SlideTransition(direction="up"))
        self.agenda = Agenda(name="agenda")
        self.todo = Todo(name="todo")
        self.colorchooser = ColorChooser(name="colorchooser")
        self.sm.add_widget(self.agenda)
        self.sm.add_widget(self.todo)
        self.sm.add_widget(self.colorchooser)
        self.sm.current = "agenda"

        self.box = BoxLayout(orientation="vertical")
        self.box.add_widget(ActionBar())
        self.box.add_widget(self.sm)

        return self.box

    def go_todo(self):
        self.sm.transition.direction = "down"
        self.sm.current = "todo"
        self.sm.current_screen.reload()

    def go_colorchooser(self):
        self.sm.transition.direction = "right"
        self.sm.current = "colorchooser"
        self.sm.current_screen.reload()

    def go_agenda(self):
        self.sm.transition.direction = "up"
        self.sm.current = "agenda"
        self.sm.current_screen.go_date()

    def build_config(self, config):
        for section, values in DEFAULT_SETTINGS.items():
            config.setdefaults(section, values)

    def build_settings(self, settings):
        settings.register_type("filepath", SettingFilePath)
        settings.register_type("configfilepath", SettingCustomConfigFilePath)
        settings.register_type("label", SettingLabel)
        for pan in SETTING_PANELS:
            settings.add_json_panel(pan[0], self.config, data=pan[1])

    def on_config_change(self, config, *args):
        getattr(self, "on_config_change_" + args[0])(config, *args)

    def on_config_change_agenda(self, config, *args):
        self.go_agenda()

    def on_config_change_ddb(self, config, section, key, value):
        self._reload_app()

    def on_config_change_aide(self, config, section, key, value):
        pass  # pragma: no cover_all

    def get_application_config(self, disable_debug=None):
        return super().get_application_config(
            str(
                Path(
                    get_dir("config", disable_debug=disable_debug), "settings.ini"
                ).absolute()
            )
        )

    def _reload_app(self):
        exec_app = [sys.executable, BASE_DIR]
        startupinfo = None
        if platform.system() == "Windows":  # pragma: no cover_linux
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.Popen(exec_app, startupinfo=startupinfo)
        self.stop()

    # def _reset_database(self):
    #     """ when something wrong with database"""
    #     cp = ConfigParser()
    #     config_file = self.get_application_config()
    #     cp.read(config_file)
    #     default = DEFAULT_SETTINGS["ddb"]["path"]
    #     cp.update({"ddb": {"path": default}})
    #     # cp["ddb"]["path"] = default
    #     with open(config_file, "wt") as f:
    #         cp.write(f)
    #     self.config = None
    #     self.load_config()
    #     self.config.update({"ddb": {"path": default}})
    #
    #     mydevoirs.database.db = init_database(filename=default, create_db=True)
