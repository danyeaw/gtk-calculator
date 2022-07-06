import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Calculator")
        grid = Gtk.Grid()
        self.set_child(grid)
        self.operand_a = None
        self.operand_b = None
        self.operator = None

        number_box = Gtk.Box()
        self.number = Gtk.Label()
        number_box.append(self.number)
        grid.attach(number_box, 0, 0, 3, 1)

        operator_text_box = Gtk.Box()
        self.operator_text = Gtk.Label()
        operator_text_box.append(self.operator_text)
        grid.attach(operator_text_box, 0, 1, 3, 1)

        # Add numeral buttons
        for num in range(9):
            floor_div_3, modulo_3 = divmod(num, 3)
            self.add_num_button(str(num), modulo_3, floor_div_3 + 2)
        self.add_num_button("0", 1, 5)

        # Add operator buttons
        operators = ("+", "-", "x", "/")
        for operator_row, operator in enumerate(operators, start=2):
            button = Gtk.Button.new_with_label(operator)
            button.connect("clicked", self.on_operator_clicked)
            button.show()
            grid.attach(button, 3, operator_row, 1, 1)

        # Add equal button
        equal_button = Gtk.Button.new_with_label("=")
        equal_button.connect("clicked", self.on_equal_clicked)
        equal_button.show()
        grid.attach(equal_button, 2, 5, 1, 1)

        # Add clear button
        clear_button = Gtk.Button.new_with_label("C")
        clear_button.connect("clicked", self.on_clear_clicked)
        clear_button.show()
        grid.attach(clear_button, 0, 5, 1, 1)

    def add_num_button(self, label: str, column: int, row: int):
        button = Gtk.Button.new_with_label(label)
        button.connect("clicked", self.on_number_clicked)
        button.show()
        self.get_child().attach(button, column, row, 1, 1)

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


def on_close(button: Gtk.Button):
    app.quit()


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


if __name__ == "__main__":
    app = MyApp(application_id="com.example.GtkApplication")
    app.run(sys.argv)
