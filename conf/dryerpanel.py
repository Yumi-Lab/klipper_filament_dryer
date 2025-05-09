import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ks_includes.screen_panel import ScreenPanel
from ks_includes.KlippyGcodes import KlippyGcodes


class Panel(ScreenPanel):
    def __init__(self, screen, title, **kwargs):
        title = title or _("Dryer Manager")
        super().__init__(screen, title, **kwargs)
        self.menu = ['dryerpanel']
        self.yms_list = self.get_yms_heaters()
        self.labels['dryerpanel'] = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.make_ui()
        self.content.add(self.labels['dryerpanel'])

    def get_yms_heaters(self):
        # Extract heater names that contain 'YMS'
        return [
            name for name in self._printer.get_heaters()
            if "YMS" in name
        ]

    def make_ui(self):
        grid = self.labels['dryerpanel']
        for idx, heater in enumerate(self.yms_list):
            label = Gtk.Label(label=f"{heater}: {self.get_temp_display(heater)}")
            label.set_halign(Gtk.Align.START)

            btn_pla = Gtk.Button(label="PLA")
            btn_pla.connect("clicked", self.run_preset_macro, heater, "pla")

            btn_petg = Gtk.Button(label="PETG")
            btn_petg.connect("clicked", self.run_preset_macro, heater, "petg")

            btn_config = Gtk.Button(label="Personnaliser")
            btn_config.connect("clicked", self.open_config_panel, heater)

            row = idx
            grid.attach(label, 0, row, 1, 1)
            grid.attach(btn_pla, 1, row, 1, 1)
            grid.attach(btn_petg, 2, row, 1, 1)
            grid.attach(btn_config, 3, row, 1, 1)

    def get_temp_display(self, heater_name):
        try:
            temp = self._printer.get_stat(heater_name, "temperature")
            return f"{temp:.1f}°C"
        except:
            return "?°C"

    def run_preset_macro(self, button, heater_name, material):
        macro = {
            "pla": "START_DRYER TEMP=45 MINUTES=360",
            "petg": "START_DRYER TEMP=80 MINUTES=360",
        }.get(material, "")
        if macro:
            yms_id = heater_name.split("-")[-1]
            script = f"{macro} YMS={yms_id}"
            self._screen._send_action(button, "printer.gcode.script", {"script": script})

    def open_config_panel(self, button, heater_name):
        self.set_panel("dryer_config", heater=heater_name)
