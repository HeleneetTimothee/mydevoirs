from kivy.uix.settings import SettingPath
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.filebrowser import FileBrowser
import os

from kivy.uix.popup import Popup
from mydevoirs.ouinonpopup import OuiNonPopup
from pathlib import Path

"""
SettingsPath using  Filebrowser instead Filechooser
"""


class SettingFilePath(SettingPath):
    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.filename
        if not value:
            return
        self.new_value = os.path.realpath(value)
        if self.new_value == self.value:
            return

        OuiNonPopup(
            title="Copier le contenu de l'ancienne base de donnée vers la nouvelle ?",
            on_oui=self._copy_ddb,
            on_non=self._update_value,
        )

    def _copy_ddb(self, *args):
        def write(*args):
            new.write_bytes(old.read_bytes())
            self._update_value()

        old = Path(self.value)
        new = Path(self.new_value)
        if new.exists():
            OuiNonPopup(
                title=f"Confirmez le remplacement du contenu de {str(new)} par {str(old)}",
                on_oui=write,
                on_non=self._dismiss,
            )
        else:
            self._update_value()

    def _update_value(self, *args):
        print("call")
        self.value = self.new_value

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation="vertical", spacing=5)
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(1, 0.9)
        )

        # create the filechooser
        initial_path = self.value or os.getcwd()

        self.textinput = textinput = FileBrowser(
            path=initial_path, size_hint=(1, 1), dirselect=False, show_hidden=True
        )
        textinput.bind(on_success=self._validate)
        textinput.bind(on_submit=self._validate)
        textinput.bind(on_canceled=self._dismiss)

        # construct the content
        content.add_widget(textinput)
        popup.open()
