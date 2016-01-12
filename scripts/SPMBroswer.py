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
from Navigator import Navigator
from Imager import Imager
from Infor import Infor
from Operator import Operator
from GwyData import GwyData

# Class for navigation
class SPMBrowser():
    def __init__(self):
        # Definiton of the variables
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.path_selected = None
        self.navi = Navigator(self.window)
        self.info = Infor(self.window)
        self.oper = Operator(self.window)
        self.gwydata = GwyData()
        self.img_1 = Imager(self.window,400)
        self.img_2 = Imager(self.window,400)
        self.channel_img_1 = None
        self.channel_img_2 = None
        # Definition of the widget
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.set_title("SPMBrowser")
        # vbox_main
        self.vbox_main = gtk.VBox(False,0)
        # hbox_main
        self.hbox_main = gtk.HBox(False,0)
        self.vbox_2 = gtk.VBox(False,0)
        self.hbox_main.pack_start(self.img_1.vbox_main,1,1,0)
        self.hbox_main.pack_start(self.img_2.vbox_main,1,1,0)
        self.vbox_2.pack_start(self.info.table_info,0,1,0)
        self.vbox_2.pack_end(self.oper.vbox_main,0,1,0)
        self.hbox_main.pack_end(self.vbox_2,0,1,0)
        # pack
        self.vbox_main.pack_start(self.navi.vbox_main,0,1,0)
        self.vbox_main.pack_start(self.hbox_main,0,1,0)
        self.window.add(self.vbox_main)
        self.window.show_all()
        # Signal handling
        self.navi.combobox_files.connect('changed',self.update_all,None)
        self.img_1.combobox_channels.connect('changed',self.record_channels,None)
        self.img_2.combobox_channels.connect('changed',self.record_channels,None)
        self.window.connect('key_press_event',self._key_press_event)

    def update_all(self,widget,data):
        self.current_data = self.navi.get_full_path()
        #self.channel_img_1 = self.img_1.get_active_channel()
        #self.channel_img_2 = self.img_2.get_active_channel()

        if self.current_data:
            self.gwydata.load_data(self.current_data)
            self.info.initialize(widget,self.gwydata.param)
            #print self.gwydata.param['channels']
            self.oper.get_current_data(self.current_data,self.navi.path2save)
            self.img_1.initialize(self.gwydata.get_container(),self.gwydata.get_param(),self.channel_img_1)
            self.img_2.initialize(self.gwydata.get_container(),self.gwydata.get_param(),self.channel_img_2)

    def record_channels(self,widget,data):
        self.channel_img_1 = self.img_1.get_active_channel()
        self.channel_img_2 = self.img_2.get_active_channel()

    def _key_press_event(self,widget,data):
        keyval = data.keyval
        #print keyval
        if keyval == 110:
            active = self.navi.combobox_files.get_active()
            if active >= 0:
                self.navi.go_forward(widget,data)
        if keyval == 98:
            active = self.navi.combobox_files.get_active()
            if active >= 0:
                self.navi.go_backward(widget,data)

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    SPMBrowser()
    main()
