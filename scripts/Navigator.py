#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import sys
import os
sys.path.insert(1,"/usr/local/lib64/python2.7/site-packages")

def sorted_ls(path, files):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(files, key=mtime))

# Class for navigation
class Navigator():
    def __init__(self,parent):
        self.parent = parent
        # Definiton of the variables
        self.path_selected = None
        self.files = None
        self.path2save = None
        self.active = None
        self.text = None
        self.current_data = None
        # Definition of the widget
        # Main widget
        self.vbox_main = gtk.VBox(False,0)
        self.hbox_1 = gtk.HBox(False,0)
        self.hbox_2 = gtk.HBox(False,0)
        self.vbox_main.pack_start(self.hbox_1,1,1,0)
        self.vbox_main.pack_start(self.hbox_2,1,1,0)
        # hbox 1
        self.combobox_files = gtk.combo_box_new_text()
        self.button_first = gtk.Button("<|")
        self.button_backward = gtk.Button("  <  ")
        self.button_forward = gtk.Button("  >  ")
        self.button_last = gtk.Button("|>")
        self.button_load = gtk.Button("Load")
        self.hbox_1.pack_start(self.combobox_files,1,1,0)
        self.hbox_1.pack_end(self.button_load,0,1,0)
        self.hbox_1.pack_end(self.button_last,0,1,0)
        self.hbox_1.pack_end(self.button_forward,0,1,0)
        self.hbox_1.pack_end(self.button_backward,0,1,0)
        self.hbox_1.pack_end(self.button_first,0,1,0)
        # hbox 2
        self.label_save_dir_pre = gtk.Label("<b>Dest</b>")
        self.label_save_dir_pre.set_use_markup(True)
        self.frame_save_dir = gtk.Frame()
        self.frame_save_dir.add(self.label_save_dir_pre)
        self.label_save_dir = gtk.Label()
        self.label_save_dir.set_alignment(0,0.5)
        self.button_default = gtk.Button("Reset")
        self.button_new_dir = gtk.Button("New")
        self.hbox_2.pack_start(self.frame_save_dir,0,1,0)
        self.hbox_2.pack_start(self.label_save_dir,1,1,0)
        self.hbox_2.pack_end(self.button_new_dir,0,1,0)
        self.hbox_2.pack_end(self.button_default,0,1,0)
        # signal handling
        self.button_load.connect("clicked",self.select_path,None)
        self.button_first.connect("clicked",self.go_first,None)
        self.button_backward.connect("clicked",self.go_backward,None)
        self.button_forward.connect("clicked",self.go_forward,None)
        self.button_last.connect("clicked",self.go_last,None)
        self.button_default.connect("clicked",self.set_path2save,None)
        self.button_new_dir.connect("clicked",self.new_path2save,None)


    def select_path(self, widget, data):
        # load image
        dialog = gtk.FileChooserDialog("Open..", self.parent,
        gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        #dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.path_selected = dialog.get_filename()
            self.update_files()
            self.set_path2save(widget,None)
            #print dialog.get_filename(), 'selected'
        elif response == gtk.RESPONSE_CANCEL:
            #print 'Closed, no files selected'
            pass
        dialog.destroy()

    def update_files(self):
        self.files = [f for f in os.listdir(self.path_selected) if os.path.isfile(self.path_selected +'/'+ f) and f[-3:] == 'sxm']
        model = self.combobox_files.get_model()
        if model:
            model.clear()
        if len(self.files) > 0:
            model = self.combobox_files.get_model()
            self.combobox_files.set_model(None)
            files_sorted = sorted_ls(self.path_selected, self.files)
            for item in files_sorted:
                #print item
                model.append([item])
                    #self.combobox_files.append_text(item)
                self.combobox_files.set_model(model)
                self.combobox_files.set_active(0)
                self.combobox_files.grab_focus()

    def set_path2save(self,widget,data):
        if self.path_selected:
            self.path2save = self.path_selected + '/temp/'
            self.label_save_dir.set_text(self.path2save)

    def get_path2save(self):
        return self.path2save

    def new_path2save(self,widget,data):
        dialog = gtk.FileChooserDialog("Open..", self.parent,
        gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        #dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.path2save = dialog.get_filename() + '/temp/'
            self.label_save_dir.set_text(self.path2save)
            #print dialog.get_filename(), 'selected'
        elif response == gtk.RESPONSE_CANCEL:
            #print 'Closed, no files selected'
            pass
        dialog.destroy()



    def go_first(self,widget,data):
        model = self.combobox_files.get_model()
        active = self.combobox_files.get_active()
        if active < 0:
            pass
        else:
            self.combobox_files.set_active(0)

    def go_backward(self,widget,data):
        model = self.combobox_files.get_model()
        active = self.combobox_files.get_active()
        if active < 0:
            pass
        elif active == 0:
            pass
        else:
            self.combobox_files.set_active(active-1)

    def go_forward(self,widget,data):
        model = self.combobox_files.get_model()
        active = self.combobox_files.get_active()
        if active < 0:
            pass
        elif active == len(self.files)-1:
            pass
        else:
            self.combobox_files.set_active(active+1)

    def go_last(self,widget,data):
        model = self.combobox_files.get_model()
        active = self.combobox_files.get_active()
        if active < 0:
            pass
        else:
            self.combobox_files.set_active(len(self.files)-1)

    def get_index(self):
        self.active = self.combobox_files.get_active()
        return self.active

    def get_text(self):
        model = self.combobox_files.get_model()
        self.active = self.combobox_files.get_active()
        self.text = model[self.active][0]
        return self.text

    def get_full_path(self):
        self.current_data = self.path_selected + '/' + self.get_text()
        return self.current_data


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    window = gtk.Window()
    navi = Navigator(window)
    print "hi"
    window.add(navi.vbox_main)
    window.show_all()
    window.present()
    main()
