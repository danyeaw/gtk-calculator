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

        self.builder = Gtk.Builder()
        self.builder.add_from_file("layout.ui")
        grid = self.builder.get_object("grid")
        self.set_child(grid)

        self.number = self.builder.get_object("number")
        self.operator_text = self.builder.get_object("operator_text")

        for num in range(9):
            button = self.builder.get_object(f"button{num}")
            button.connect("clicked", self.on_number_clicked)

        operators = ("add", "subtract", "multiply", "divide")
        for operator in operators:
            operator_button = self.builder.get_object(f"button-{operator}")
            operator_button.connect("clicked", self.on_operator_clicked)

        equal_button = self.builder.get_object("equal_button")
        equal_button.connect("clicked", self.on_equal_clicked)

        clear_button = self.builder.get_object("clear_button")
        clear_button.connect("clicked", self.on_clear_clicked)

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