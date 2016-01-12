#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import sys
sys.path.insert(1,"/usr/local/lib64/python2.7/site-packages")
import gwy
import re
import numpy as np
from GwyData import GwyData
from Navigator import Navigator

# Class for image
class Imager():
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

        # Signal handling
        self.combobox_channels.connect('changed',self.update_image,None)
        self.combobox_directions.connect('changed',self.update_image,None)

    def initialize(self,container,param,active_channel=None):
        self.c = container
        self.param = param
        self.d_origin = None
        self.channels = self.param['channels']
        #print self.channels
        model = self.combobox_channels.get_model()
        if model:
            model.clear()
        if len(self.channels) > 0:
            model = self.combobox_channels.get_model()
            self.combobox_channels.set_model(None)
            for item in self.channels:
                model.append([item])
            self.combobox_channels.set_model(model)
            if active_channel:
                if active_channel in self.channels:
                    #print self.channels, active_channel
                    active = self.channels.index(active_channel)
                    self.channel_id = active
                    self.channel_str = active_channel
            else:
                self.channel_id = 0
                self.channel_str = self.channels[self.channel_id]
            self.combobox_channels.set_active(self.channel_id)

    def get_active_channel(self):
        #print 'active_channel changed'
        model = self.combobox_channels.get_model()
        self.channel_id = self.combobox_channels.get_active()
        if not self.channel_id >=0:
            return None
        else:
            #print 'channel_id ', self.channel_id
            #print 'model ',model[self.channel_id]
            self.channel_str = model[self.channel_id][0]
            return self.channel_str

    def load_data(self):
        self.channel_id = self.combobox_channels.get_active()
        model = self.combobox_channels.get_model()
        active = self.combobox_channels.get_active()
        if active >= 0:
            self.channel_str = model[self.channel_id][0]
            #print self.channel_str
            self.direction_id = self.combobox_directions.get_active()
            data_id = self.channel_id * 2 + self.direction_id
            #print self.channel_id,self.direction_id, data_id
            self.data_id_str = '/'+str(data_id)+'/'
            self.d_origin = self.c[self.data_id_str + 'data']
            #self.d = self.d_origin.duplicate()
            if self.d_origin:
                self.c.set_object_by_name(self.data_id_str + 'data',self.d_origin)
            else:
                self.d_origin = self.c[self.data_id_str + 'data']
            gwy.gwy_app_data_browser_select_data_field(self.c,0)
            #if self.togglebutton_level.get_active():
            #    gwy.gwy_app_data_browser_select_data_field(self.c, 0)
            #    gwy.gwy_process_func_run("level", self.c, gwy.RUN_IMMEDIATE)
            self.d = self.c[self.data_id_str + 'data']
            d_process = self.d.duplicate()
            #self.data_min = self.d.get_min()
            #self.data_max = self.d.get_max()
            #self. data_dif = self.data_max - self.data_min
            #self.scale_min_current = self.scale_min.get_value()
            #self.scale_max_current = self.scale_max.get_value()
            #bottom = self.data_min + self.scale_min_current/100*self.data_dif
            #top = self.data_min + self.scale_max_current/100*self.data_dif
            #d_process.clamp(bottom, top)
            #self.d.clamp(bottom, top)
            self.d = d_process
        else:
            pass

    def update_image(self,widget,data):
        #pass
        gwy.gwy_app_data_browser_add(self.c)
        self.load_data()
        self.d.data_changed()
        #print "update", self.togglebutton_level.get_active()
        self.local_c.set_object_by_name(self.data_id_str+"data", self.d)
        if re.search(r'Z', self.channel_str):
            #print self.channel_str
            self.gradient_key = 'Julio'
        elif re.search(r'Frequency', self.channel_str):
            self.gradient_key = 'Gray'
        self.local_c.set_string_by_name(self.data_id_str+"base/palette", self.gradient_key)
        self.local_c.set_int32_by_name(self.data_id_str+"base/range-type", 1)#gwy.LAYER_BASIC_RANGE_FIXED
        #self.local_c.set_double_by_name(self.data_id_str+"base/min", float(self.data_min + self.scale_min_current/100*self.data_dif))
        #self.local_c.set_double_by_name(self.data_id_str+"base/max", float(self.data_min + self.scale_max_current/100*self.data_dif))
        self.local_c[self.data_id_str+"data"].data_changed()
        #print self.local_c[self.data_id_str+"base/min"],self.data_id_str+"base/min"
        #print self.data_min + self.scale_min_current/100*self.data_dif,self.data_min + self.scale_max_current/100*self.data_dif
        layer = gwy.LayerBasic()
        layer.set_data_key(self.data_id_str+"data")
        layer.set_gradient_key(self.data_id_str+"base/palette")
        layer.set_range_type_key(self.data_id_str+"base")
        layer.set_min_max_key(self.data_id_str+"base")
        self.view.set_data_prefix(self.data_id_str+"data")
        self.view.set_base_layer(layer)
        #self.combobox_files.grab_focus()
        gwy.gwy_app_data_browser_remove(self.c)



class TestBrowser():
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.path_selected = None
        self.navi = Navigator(self.window)
        self.img = Imager(self.window,400)
        self.gwydata = GwyData()
        self.channel_img = None
        # widget
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.set_title("TestBrowser")
        self.vbox_main = gtk.VBox(False,0)
        self.vbox_main.pack_start(self.navi.vbox_main,0,1,0)
        self.vbox_main.pack_start(self.img.vbox_main,1,1,0)
        self.window.add(self.vbox_main)
        self.window.show_all()
        # Signal handling
        self.navi.combobox_files.connect('changed',self.update_all,None)
        self.img.combobox_channels.connect('changed',self.record_channel,None)

    def update_all(self,widget,data):
        self.current_data = self.navi.get_full_path()
        if self.current_data:
            self.gwydata.load_data(self.current_data)
            self.img.initialize(self.gwydata.get_container(),self.gwydata.get_param(),self.channel_img)

    def record_channel(self,widget,data):
        self.channel_img = self.img.get_active_channel()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    TestBrowser()
    main()
