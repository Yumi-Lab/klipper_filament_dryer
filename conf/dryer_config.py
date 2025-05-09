
import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ks_includes.screen_panel import ScreenPanel
from ks_includes.KlippyGtk import NumberPadPopup
import configparser

class Panel(ScreenPanel):
    def __init__(self, screen, title, heater=None, **kwargs):
        super().__init__(screen, title, **kwargs)
        self.heater = heater
        self.set_title(f"Configurer {heater}")
        self.grid = Gtk.Grid(row_spacing=12, column_spacing=12, margin=20)
        self.grid.set_column_homogeneous(False)
        self.content = self.grid

        self.temp_button = Gtk.Button(label="Température (°C)")
        self.temp_button.connect("clicked", self.set_temperature)
        self.grid.attach(self.temp_button, 0, 0, 2, 1)

        self.time_button = Gtk.Button(label="Durée (minutes)")
        self.time_button.connect("clicked", self.set_time)
        self.grid.attach(self.time_button, 0, 1, 2, 1)

        submit_button = Gtk.Button(label="Valider")
        submit_button.get_style_context().add_class("suggested-action")
        submit_button.connect("clicked", self.submit_custom)
        self.grid.attach(submit_button, 0, 2, 2, 1)

        self.grid.show_all()
        self.temp = 45
        self.minutes = 360

    def set_temperature(self, button):
        popup = NumberPadPopup(self._screen, "Température (°C)", self.temp, self.on_temp_set)
        popup.show_all()

    def on_temp_set(self, value):
        self.temp = int(value)
        self.temp_button.set_label(f"Température : {self.temp}°C")

    def set_time(self, button):
        popup = NumberPadPopup(self._screen, "Durée (min)", self.minutes, self.on_time_set)
        popup.show_all()

    def on_time_set(self, value):
        self.minutes = int(value)
        self.time_button.set_label(f"Durée : {self.minutes} min")

    def submit_custom(self, *args):
        yms_id = self.heater.split("-")[-1]
        script = f"START_DRYER YMS={yms_id} TEMP={self.temp} MINUTES={self.minutes}"
        logging.info(f"Running custom script: {script}")
        if self._printer and self._printer.gcode:
            self._printer.gcode.run_script(script)
        else:
            logging.warning("Printer or gcode interface not available")
        self.go_back()
