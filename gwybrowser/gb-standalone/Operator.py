#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import sys
sys.path.insert(1, "/usr/local/lib64/python2.7/site-packages")
import gwy
import os
import shutil
from convert_sxm2png_text import save2png_text

# Class for navigation
class Operator():
    def __init__(self,parent):
        self.parent = parent
        # Definition of the variables
        self.c = None
        self.param = None
        self.dest_path = None
        self.channel = None
        # Definition of the widget
        self.vbox_main = gtk.VBox(False,0)
        self.button_save = gtk.Button("Save")
        self.button_save2 = gtk.Button("Save Sys")
        self.button_copy = gtk.Button("Copy")
        self.button_open = gtk.Button("Open")
        self.button_quit = gtk.Button("Quit")
        self.vbox_main.pack_start(self.button_save,0,1,0)
        self.vbox_main.pack_start(self.button_save2,0,1,0)
        self.vbox_main.pack_start(self.button_copy,0,1,0)
        self.vbox_main.pack_start(self.button_open,0,1,0)
        self.vbox_main.pack_start(self.button_quit,0,1,0)

        # Signal handling
        self.button_open.connect('clicked', self.open_file, None)
        self.button_copy.connect('clicked',self.copy_file,None)
        self.button_save.connect('clicked',self.save_file,None)
        self.button_save2.connect('clicked',self.save_file2,None)
        self.button_quit.connect('clicked',lambda w: gtk.main_quit())

    def save_file(self,widget,data):
        #print self.dest_path, self.channel
        if self.c and self.channel:
            save2png_text(self.c,self.param,self.channel)
            #self.combobox_files.grab_focus()

    def save_file2(self,widget,data):
        file_name = self.param['full_path'] + '.png'

    def copy_file(self,widget,data):
        if self.c:
            #self.save_file()
            if self.dest_path:
                shutil.copy(self.param['full_path'],self.dest_path+os.path.basename(self.param['full_path']))
                print self.param['full_path'],'copied to',self.dest_path+os.path.basename(self.param['full_path'])
            else:
                shutil.copy(self.param['full_path'],os.path.dirname(self.param['full_path'])+'/temp/'+os.path.basename(self.param['full_path']))
                print self.param['full_path'],'copied to',os.path.dirname(self.param['full_path'])+'/temp/'+os.path.basename(self.param['full_path'])

    def open_file(self,widget,data):
        if self.current_data:
            #self.current_data = data
            gwy.gwy_app_file_load(self.current_data)

    def get_current_data(self,container,param,dest_path,channel):
        #print dest_path,channel
        self.c = container
        self.param = param
        self.dest_path = dest_path
        self.channel = channel

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
