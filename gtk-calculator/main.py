import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Calculator")
        self.stack: list[int] = []
        self.value_complete: bool = False

        callback_mapping = {
            "on_number_clicked": self.on_number_clicked,
            "on_operator_clicked": self.on_operator_clicked,
            "on_clear_clicked": self.on_clear_clicked,
        }
        self.builder = Gtk.Builder(callback_mapping)
        self.builder.add_from_file("layout.ui")
        grid = self.builder.get_object("grid")
        self.set_child(grid)

        self.last_in_display = self.builder.get_object("last_in_display")
        self.first_in_display = self.builder.get_object("first_in_display")

    def on_number_clicked(self, button: Gtk.Button) -> None:
        value = button.get_label()
        if self.value_complete:
            self.first_in_display.set_text(self.last_in_display.get_text())
            self.last_in_display.set_text("")
            self.value_complete = False
        self.last_in_display.set_text(self.last_in_display.get_text() + value)

    def on_operator_clicked(self, button: Gtk.Button) -> None:
        if current_value := self.last_in_display.get_text():
            self.stack.append(int(current_value))
            self.value_complete = True
        operator = button.get_label()
        if operator != "enter" and len(self.stack) >= 2:
            self.perform_operation(operator)

    def perform_operation(self, operator: str) -> None:
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        result = eval(f"{operand_a} {operator} {operand_b}")
        self.first_in_display.set_text("")
        self.stack.append(result)
        self.last_in_display.set_text(str(result))

    def on_clear_clicked(self, button: Gtk.Button) -> None:
        self.last_in_display.set_text("")
        self.first_in_display.set_text("")
        self.stack = []


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
