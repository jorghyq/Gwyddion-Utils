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
class MultiImager():
    def __init__(self,parent,number):
        self.parent = parent
        self.number = number
        # Definition of the variables
        self.current_data = None
        self.channel_id = 0
        self.channels = None
        self.direction_id = 0
        self.files = None
        self.path_selected = None
        self.current_data_id = None
        self.containers = []
        self.views = []
        self.files2show = None
        self.gwydatas = []
        # Definition of the widget
        self.hbox_main = gtk.HBox(False,0)
        for i in range(self.number):
            container = gwy.Container()
            view = gwy.DataView(container)
            gwydata = GwyData()
            view.set_size_request(150,150)
            self.containers.append(container)
            self.views.append(view)
            self.gwydatas.append(gwydata)
        for item in self.views:
            self.hbox_main.pack_start(item,1,1,0)

    def initialize(self,path_selected,files,current_data_id):
        self.files = files
        file_num = len(files)
        self.files2show = []
        self.path_selected = path_selected
        self.current_data_id = current_data_id
        if self.current_data_id > file_num - self.number:
            for i in range(self.number):
                self.files2show.append(self.files[file_num-self.number+i])
        else:
            for i in range(self.number):
                self.files2show.append(self.files[self.current_data_id+i])
        for i in range(self.number):
            print self.path_selected + '/' + self.files2show[i]
            self.gwydatas[i].load_data(self.path_selected+'/'+self.files2show[i])

    #def get_active_(self,channel,direction):
    #    self.channel_id

    def load_data(self,channel_id,direction_id):
        self.channel_id = channel_id
        self.direction_id = direction_id
        if self.channel_id >= 0:
            #print self.channel_str
            data_id = self.channel_id * 2 + self.direction_id
            #print self.channel_id,self.direction_id, data_id
            self.data_id_str = '/'+str(data_id)+'/'
        else:
            pass

    def update_image(self,widget,data):
        #pass
        for container,gwydata,view in zip(self.containers,self.gwydatas,self.views):
            self.c = gwydata.get_container()
            self.load_data(0,0)
            gwy.gwy_app_data_browser_add(self.c)
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
            self.d.data_changed()
            #print "update", self.togglebutton_level.get_active()
            container.set_object_by_name(self.data_id_str+"data", self.d)
            #if re.search(r'Z', self.channel_str):
                #print self.channel_str
            #    self.gradient_key = 'Julio'
            self.gradient_key = 'Julio'
            #elif re.search(r'Frequency', self.channel_str):
            #    self.gradient_key = 'Gray'
            container.set_string_by_name(self.data_id_str+"base/palette", self.gradient_key)
            container.set_int32_by_name(self.data_id_str+"base/range-type", 1)#gwy.LAYER_BASIC_RANGE_FIXED
            #self.local_c.set_double_by_name(self.data_id_str+"base/min", float(self.data_min + self.scale_min_current/100*self.data_dif))
            #self.local_c.set_double_by_name(self.data_id_str+"base/max", float(self.data_min + self.scale_max_current/100*self.data_dif))
            container[self.data_id_str+"data"].data_changed()
            #print self.local_c[self.data_id_str+"base/min"],self.data_id_str+"base/min"
            #print self.data_min + self.scale_min_current/100*self.data_dif,self.data_min + self.scale_max_current/100*self.data_dif
            layer = gwy.LayerBasic()
            layer.set_data_key(self.data_id_str+"data")
            layer.set_gradient_key(self.data_id_str+"base/palette")
            layer.set_range_type_key(self.data_id_str+"base")
            layer.set_min_max_key(self.data_id_str+"base")
            view.set_data_prefix(self.data_id_str+"data")
            view.set_base_layer(layer)
            #self.combobox_files.grab_focus()
            gwy.gwy_app_data_browser_remove(self.c)



class TestBrowser():
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.path_selected = None
        self.navi = Navigator(self.window)
        self.mimg = MultiImager(self.window,4)
        self.gwydata = GwyData()
        self.channel_img = None
        # widget
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.set_title("TestBrowser")
        self.vbox_main = gtk.VBox(False,0)
        self.vbox_main.pack_start(self.navi.vbox_main,0,1,0)
        self.vbox_main.pack_start(self.mimg.hbox_main,1,1,0)
        self.window.add(self.vbox_main)
        self.window.show_all()
        # Signal handling
        self.navi.combobox_files.connect('changed',self.update_all,None)

    def update_all(self,widget,data):
        self.current_data = self.navi.get_full_path()
        if self.current_data:
            self.mimg.initialize(self.navi.path_selected,self.navi.files,self.navi.get_index())
            self.mimg.update_image(widget,None)

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    TestBrowser()
    main()
