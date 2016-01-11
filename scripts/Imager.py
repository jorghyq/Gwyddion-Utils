#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gobject
import gtk
import sys
sys.path.insert(1,"/usr/local/lib64/python2.7/site-packages")
import gwy
import re
import numpy as np


# Class for image
class Imager():
    __gtype_name__ = 'Imager'

    def __init__(self,parent,size):
        self.parent = parent
        # Definition of the variables
        self.current_data = None
        self.channel_str = None
        self.channel_id = 0
        self.channels = None
        self.direction_str = None
        self.direction_id = 0
        self.param = None

        # Definition of the widget
        self.vbox_main = gtk.VBox(False,0)
        self.hbox_main = gtk.HBox(False,0)
        self.local_c = gwy.Container()
        self.view = gwy.DataView(self.local_c)
        self.view.set_size_request(size,size)
        self.vbox_main.pack_start(self.hbox_main,0,1,0)
        self.vbox_main.pack_start(self.view,1,1,0)
        # Definition of the hbox_main
        self.combobox_channels = gtk.combo_box_new_text()
        self.combobox_directions = gtk.combo_box_new_text()
        self.combobox_directions.append_text("Forward")
        self.combobox_directions.append_text("Backward")
        self.combobox_directions.set_active(0)
        self.label_channels = gtk.Label("<b>Channel: </b>")
        self.label_channels.set_use_markup(True)
        self.label_directions = gtk.Label("<b>Direction: </b>")
        self.label_directions.set_use_markup(True)
        self.hbox_main.pack_start(self.label_channels,0,1,0)
        self.hbox_main.pack_start(self.combobox_channels,0,1,0)
        self.hbox_main.pack_end(self.combobox_directions,0,1,0)
        self.hbox_main.pack_end(self.label_directions,0,1,0)

    def initialize(self,container,param):
        self.c = container
        self.param = param
        self.channels = self.param['channels']
        active = self.combobox_channels.get_active()
        if active < 0:
            pass
        else:
            model = self.combobox_channels.get_model()
            self.combobox_channels.set_model(None)
            model.clear()
            for item in self.channels:
                model.append([item])
            self.combobox_channels.set_model(model)
            self.combobox_channels.set_active(self.channel_id)
            self.channel_str = model[self.channel_id][0]

    def update_image(self,widget,data):
        gwy.gwy_app_data_browser_add(self.c)












def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    window = gtk.Window()
    im = Imager(window,300)
    print "hi"
    window.add(im.vbox_main)
    window.show_all()
    window.present()
    main()
