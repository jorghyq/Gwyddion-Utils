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
from GwyData import GwyData
# Class for navigation
class Infor():
    def __init__(self,parent):
        self.parent = parent
        # Definiton of the variables
        self.c = None
        self.param = None
        self.table_info = gtk.Table(4,2,True)
        self.label_volt_pre = gtk.Label("V: ")
        self.label_current_pre = gtk.Label("I: ")
        self.label_w_pre = gtk.Label("W: ")
        self.label_h_pre = gtk.Label("H: ")
        self.label_volt = gtk.Label(None)
        self.label_current = gtk.Label(None)
        self.label_w = gtk.Label(None)
        self.label_h = gtk.Label(None)
        self.frame_volt = gtk.Frame()
        self.frame_volt.add(self.label_volt_pre)
        self.frame_current = gtk.Frame()
        self.frame_current.add(self.label_current_pre)
        self.frame_w = gtk.Frame()
        self.frame_w.add(self.label_w_pre)
        self.frame_h = gtk.Frame()
        self.frame_h.add(self.label_h_pre)
        self.label_types =gtk.Label("Type: ")
        self.combobox_types =gtk.combo_box_new_text()
        types = ["Unknown","Metal","Molecules","Useless"]
        for item in types:
            self.combobox_types.append_text(item)
            self.combobox_types.set_active(0)
        self.table_info.attach(self.frame_volt,0,1,0,1)
        self.table_info.attach(self.label_volt,1,2,0,1)
        self.table_info.attach(self.frame_current,0,1,1,2)
        self.table_info.attach(self.label_current,1,2,1,2)
        self.table_info.attach(self.frame_w,0,1,2,3)
        self.table_info.attach(self.label_w,1,2,2,3)
        self.table_info.attach(self.frame_h,0,1,3,4)
        self.table_info.attach(self.label_h,1,2,3,4)
        self.table_info.attach(self.label_types,0,1,4,5)
        self.table_info.attach(self.combobox_types,1,2,4,5)

    def initialize(self,widget,data):
        #self.c = container
        self.param = data
        self.label_volt.set_text(self.param['bias']+' '+ self.param['bu'])
        self.label_current.set_text(str(self.param['current']) +' '+ self.param['cu'])
        self.label_w.set_text("{0:.1f}".format(self.param['width']) +' '+ self.param['xyu']+'['+str(self.param['w_dim'])+']')
        self.label_h.set_text("{0:.1f}".format(self.param['height']) +' '+ self.param['xyu']+'['+str(self.param['h_dim'])+']')

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    window = gtk.Window()
    data = GwyData()
    data.load_data('/home/jorghyq/Project/Gwyddion-Utils/A151201.000102-01691.sxm')
    inf = Infor(window)
    inf.initialize(data.c,data.param)
    print "hi"
    window.add(inf.table_info)
    window.show_all()
    window.present()
    main()
