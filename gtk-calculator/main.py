import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Calculator")
        self.grid = Gtk.Grid()
        self.set_child(self.grid)
        number = Gtk.Text()
        operator_text = Gtk.Text()
        number.show()
        operator_text.show()

        self.grid.attach(number, 0, 0, 3, 1)
        self.grid.attach(operator_text, 0, 1, 3, 1)

        self.add_num_button("1", 0, 2)
        self.add_num_button("2", 1, 2)
        self.add_num_button("3", 2, 2)
        self.add_num_button("4", 0, 3)
        self.add_num_button("5", 1, 3)
        self.add_num_button("6", 2, 3)
        self.add_num_button("7", 0, 4)
        self.add_num_button("8", 1, 4)
        self.add_num_button("9", 2, 4)
        self.add_num_button("0", 1, 5)

        operators = ("+", "-", "x", "/")
        for operator_row, operator in enumerate(operators, start=2):
            button = Gtk.Button.new_with_label(operator)
            button.connect("clicked", self.on_number_clicked)
            button.show()
            self.grid.attach(button, 3, operator_row, 1, 1)

        equal_button = Gtk.Button.new_with_label("=")
        equal_button.connect("clicked", self.on_equal_clicked)
        equal_button.show()
        self.grid.attach(equal_button, 2, 5, 1, 1)

        clear_button = Gtk.Button.new_with_label("C")
        clear_button.connect("clicked", self.on_clear_clicked)
        clear_button.show()
        self.grid.attach(clear_button, 0, 5, 1, 1)

    def add_num_button(self, label: str, column: int, row: int):
        button = Gtk.Button.new_with_label(label)
        button.connect("clicked", self.on_number_clicked)
        button.show()
        self.grid.attach(button, column, row, 1, 1)

    def on_number_clicked(self, button: Gtk.Button):
        print(f"Number button {button.get_label()} clicked")

    def on_operator_clicked(self, button: Gtk.Button):
        print(f"Operator button {button.get_name()} clicked")

    def on_equal_clicked(self, button: Gtk.Button):
        print(f"Equal button {button.get_name()} clicked")

    def on_clear_clicked(self, button: Gtk.Button):
        print(f"Clear button {button.get_name()} clicked")


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
