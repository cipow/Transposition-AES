import gi, time, os, math
from lib import transposition, AESlib
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainGUI(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Columnar Transposition and AES Chiper")
        self.set_border_width(10)
        self.set_default_size(200, 200)

        grid = Gtk.Grid()
        self.add(grid)
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

        # Label Notification
        self.labelNotification = Gtk.Label("")

        # Emtpy space
        empty1 = Gtk.Label("")
        empty2 = Gtk.Label("")

        ## Grid Layout
        grid.attach(self.buttonChooseFile, 0, 0, 2, 1)
        grid.attach_next_to(labelEntryKey, self.buttonChooseFile, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.entryKey, labelEntryKey, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(labelMethod, labelEntryKey, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.comboBoxMethod, labelMethod, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(empty1, 0, 4, 2, 1)
        grid.attach_next_to(buttonStart, empty1, Gtk.PositionType.BOTTOM, 2, 1)
        grid.attach_next_to(empty2, buttonStart, Gtk.PositionType.BOTTOM, 2, 1)
        grid.attach_next_to(self.labelNotification, empty2, Gtk.PositionType.BOTTOM, 2, 1)

    def on_button_start(self, widget):
        key = self.entryKey.get_text()
        method = self.comboBoxMethod.get_active_text()

        if method == 'encrypt':
            if os.path.basename(self.fileObj).startswith("(encrypt)"):
                print("This file already encryption")
                self.labelNotification.set_label("This file already encryption")

            else:
                startTime = time.time()
                with open(self.fileObj, 'r') as objectFile:
                    content = objectFile.read()

                translated = transposition.encryptMessage(int(key), content)
                outputFilename = os.path.join(
                                    os.path.dirname(self.fileObj),
                                    "tmp(encrypt)"+os.path.basename(self.fileObj))

                with open(outputFilename, 'w') as outputFileObj:
                    outputFileObj.write(translated)
                    os.remove(self.fileObj)

                AESlib.encrypt(key, outputFilename)
                os.remove(outputFilename)
                totalTime = round(time.time() - startTime, 2)
                print('%sion time: %s seconds' % (method, totalTime))
                self.labelNotification.set_label("Done\n%sion time: %s seconds" % (method, totalTime))

        else:
            if os.path.basename(self.fileObj).startswith("(encrypt)"):
                startTime = time.time()
                outputAESFile = AESlib.decrypt(key, self.fileObj)
                os.remove(self.fileObj)

                with open(outputAESFile, 'r') as objectFile:
                    content = objectFile.read()

                translated = transposition.decryptMessage(int(key), content)
                outputFilename = os.path.join(
                                    os.path.dirname(outputAESFile),
                                    os.path.basename(outputAESFile)[5:])

                with open(outputFilename, 'w') as outputFileObj:
                    outputFileObj.write(translated)
                    os.remove(outputAESFile)

                totalTime = round(time.time() - startTime, 2)
                print('%sion time: %s seconds' % (method, totalTime))
                self.labelNotification.set_label("Done\n%sion time: %s seconds" % (method, totalTime))

            else:
                print("This file not encryption")
                self.labelNotification.set_label("This file not encryption")

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


win = MainGUI()
win.set_position(Gtk.WindowPosition.CENTER)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
