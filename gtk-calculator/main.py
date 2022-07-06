import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Calculator")
        self.operand_a = None
        self.operand_b = None
        self.operator = None

        callback_mapping = {
            "on_number_clicked": self.on_number_clicked,
            "on_equal_clicked": self.on_equal_clicked,
            "on_operator_clicked": self.on_operator_clicked,
            "on_clear_clicked": self.on_clear_clicked,
        }
        self.builder = Gtk.Builder(callback_mapping)
        self.builder.add_from_file("layout.ui")
        grid = self.builder.get_object("grid")
        self.set_child(grid)

        self.number = self.builder.get_object("number")
        self.operator_text = self.builder.get_object("operator_text")

    def on_number_clicked(self, button: Gtk.Button):
        number_clicked = button.get_label()
        # First operand still being entered
        if not self.operand_a:
            self.number.set_text(self.number.get_text() + number_clicked)
        elif not self.operator:
            self.operator = self.operator_text.get_text()
            self.number.set_text(f"{self.operand_a} {self.operator}")
            self.operator_text.set_text(number_clicked)
        else:
            self.operator_text.set_text(self.operator_text.get_text() + number_clicked)

    def on_operator_clicked(self, button: Gtk.Button):
        self.operator_text.set_text(button.get_label())
        self.operand_a = int(self.number.get_text())

    def on_equal_clicked(self, button: Gtk.Button):
        self.operand_b = int(self.operator_text.get_text())
        match self.operator:
            case "+":
                result = self.operand_a + self.operand_b
            case "-":
                result = self.operand_a - self.operand_b
            case "x":
                result = self.operand_a * self.operand_b
            case _:
                result = self.operand_a / self.operand_b
        self.number.set_text(str(result))
        self.operator_text.set_text("=")

    def on_clear_clicked(self, button: Gtk.Button):
        self.number.set_text("")
        self.operator_text.set_text("")
        self.operator = None
        self.operand_a = None


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


if __name__ == "__main__":
    app = MyApp()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)