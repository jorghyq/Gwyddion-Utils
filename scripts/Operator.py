#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gobject
import gtk
import sys
import os
sys.path.insert(1,"/usr/local/lib64/python2.7/site-packages")
import gwy
import re
import numpy as np

# Class for navigation
class Operator():
    __gtype_name__ = 'Operator'

    def __init__(self,parent):
        self.parent = parent
        # Definition of the variables
        self.current_data = None
        # Definition of the widget
        self.vbox_main = gtk.VBox(False,0)
        self.button_save = gtk.Button("Save")
        self.button_copy = gtk.Button("Copy")
        self.button_open = gtk.Button("Open")
        self.button_quit = gtk.Button("Quit")
        self.vbox_main.pack_start(self.button_save,0,1,0)
        self.vbox_main.pack_start(self.button_copy,0,1,0)
        self.vbox_main.pack_start(self.button_open,0,1,0)
        self.vbox_main.pack_start(self.button_quit,0,1,0)

        # Signal handling
        self.button_open.connect('clicked', self.open_file, None)
        self.button_copy.connect('clicked',self.copy_file,None)
        self.button_save.connect('clicked',self.save_file,None)
        self.button_quit.connect('clicked',lambda w: gtk.main_quit())

    def save_file(self,widget,data):
        #self.current_data = data
        save2png_text(self.current_data,'temp')
        self.combobox_files.grab_focus()

    def copy_file(self,widget,data):
        pass

    def open_file(self,widget,data):
        #self.current_data = data
        gwy.gwy_app_file_load(self.current_data)

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    window = gtk.Window()
    oper = Operator(window)
    print "hi"
    window.add(oper.vbox_main)
    window.show_all()
    window.present()
    main()
