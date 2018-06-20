import gi, time, os, math
from lib import transposition
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainGUI(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Transposition Chiper")
        self.set_border_width(10)
        self.set_default_size(200, 200)

        grid = Gtk.Grid()
        self.add(grid)
        self.content = None
        self.fileObj = None

        ## Object

        # Choose File
        self.buttonChooseFile = Gtk.Button("Select a file")
        self.buttonChooseFile.connect("clicked", self.on_button_choose_file_clicked)

        # Entry Key
        labelEntryKey = Gtk.Label("Insert Key")
        self.entryKey = Gtk.Entry()

        # Method
        labelMethod = Gtk.Label('Choose Method')
        self.comboBoxMethod = Gtk.ComboBoxText()
        self.comboBoxMethod.append_text("encrypt")
        self.comboBoxMethod.append_text("decrypt")
        self.comboBoxMethod.set_active(0)

        # Start
        buttonStart = Gtk.Button("Start")
        buttonStart.connect("clicked", self.on_button_start)

        # Emtpy space
        empty = Gtk.Label("")

        ## Grid Layout
        grid.attach(self.buttonChooseFile, 0, 0, 2, 1)
        grid.attach_next_to(labelEntryKey, self.buttonChooseFile, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.entryKey, labelEntryKey, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(labelMethod, labelEntryKey, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.comboBoxMethod, labelMethod, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(empty, 0, 4, 2, 1)
        grid.attach_next_to(buttonStart, empty, Gtk.PositionType.BOTTOM, 2, 1)

    def on_button_start(self, widget):
        key = self.entryKey.get_text()
        method = self.comboBoxMethod.get_active_text()
        print(key+" "+method)

        if method == 'encrypt':
            translated = transposition.encryptMessage(int(key), self.content)
            outputFilename = os.path.join(
                                os.path.dirname(self.fileObj),
                                "(encrypt)"+os.path.basename(self.fileObj))
        else:
            translated = transposition.decryptMessage(int(key), self.content)
            outputFilename = os.path.join(
                                os.path.dirname(self.fileObj),
                                os.path.basename(self.fileObj)[9:])

        with open(outputFilename, 'w') as outputFileObj:
            outputFileObj.write(translated)
            os.remove(self.fileObj)

    def on_button_choose_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.buttonChooseFile.set_label(os.path.basename(dialog.get_filename()))

            if os.path.exists(dialog.get_filename()):
                with open(dialog.get_filename()) as fileObj:
                    self.content = fileObj.read()

                self.fileObj = dialog.get_filename()
                print("File is found")

            else:
                print("File is not found")

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
