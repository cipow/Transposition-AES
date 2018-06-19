import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainGUI(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Transposition Chiper")
        self.set_border_width(10)
        self.set_default_size(200, 200)

        grid = Gtk.Grid()
        self.add(grid)

        ## Object

        # Choose File
        self.buttonChooseFile = Gtk.Button("Select a file")
        self.buttonChooseFile.connect("clicked", self.on_button_choose_file_clicked)

        # Entry Key
        labelEntryKey = Gtk.Label("Insert Key")
        entryKey = Gtk.Entry()

        # Method
        labelMethod = Gtk.Label('Choose Method')
        comboBoxMethod = Gtk.ComboBoxText()
        comboBoxMethod.append_text("encrypt")
        comboBoxMethod.append_text("decrypt")
        comboBoxMethod.set_active(0)

        # Start
        buttonStart = Gtk.Button("Start")

        # Emtpy space
        empty = Gtk.Label("")

        ## Grid Layout
        grid.attach(self.buttonChooseFile, 0, 0, 2, 1)
        grid.attach_next_to(labelEntryKey, self.buttonChooseFile, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(entryKey, labelEntryKey, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(labelMethod, labelEntryKey, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(comboBoxMethod, labelMethod, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(empty, 0, 4, 2, 1)
        grid.attach_next_to(buttonStart, empty, Gtk.PositionType.BOTTOM, 2, 1)


    def on_button_choose_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.buttonChooseFile.set_label(dialog.get_filename())
            if os.path.exists(dialog.get_filename()):
                print("True")
            else:
                print("False")
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


win = MainGUI()
win.set_position(Gtk.WindowPosition.CENTER)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
