#!/usr/bin/env python
# Image Browser for Gwyddion

import pygtk
pygtk.require('2.0')
import gtk
import gwy
import os
import numpy as np
import re
from convert_sxm2png_text import save2png_text

def sorted_ls(path, files):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(files, key=mtime))

class ImageBrowser:
    def __init__(self):
	########### Initialize some variables ##############
	self.CHANNEL = None
	self.DIRECTION = None
	
	########### Initialize gui #########################
	self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.window.connect("destroy", lambda w: gtk.main_quit())
	self.window.set_title("Image Browser")
	########################## main vbox
	self.vbox_main = gtk.VBox(False, 0)
	self.hbox_main = gtk.HBox(False, 0)
	########################## hbox for file selection
	self.hbox_files = gtk.HBox(False,0)
	self.combobox_files = gtk.combo_box_new_text()
	self.button_load = gtk.Button("Load")
	self.hbox_files.pack_start(self.combobox_files,expand=True,fill=True,padding=0)
	self.hbox_files.pack_end(self.button_load,expand=False,fill=True,padding=0)
	##################### hbox holding image
	self.local_c = gwy.Container()
	self.view = gwy.DataView(self.local_c)
	#self.hbox_image = gtk.HBox(False, 0)
	#self.hbox_image.set_size_request(400, 400)
	self.view.set_size_request(400, 400)
	#self.hbox_image.set_usize(400, 400)
	#self.hbox_image.pack_start(self.view,expand=True,fill=True,padding=0)
	#self.hbox_image.set_bord(50)
	# vbox holding labels and operations
	self.vbox_ops = gtk.VBox(False,0)
	#self.vbox_ops.set_border_width(50)
	######################### elements for vbox_ops ####
	self.combobox_channels = gtk.combo_box_new_text()
	self.combobox_directions = gtk.combo_box_new_text()
	self.combobox_directions.append_text("Forward")
	self.combobox_directions.append_text("Backward")
	self.combobox_directions.set_active(0)
	self.label_channels = gtk.Label("Channel: ")
	self.label_directions = gtk.Label("Direction: ")
	self.table_info = gtk.Table(6,2,True)
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
	self.table_info.attach(self.label_channels,0,1,0,1)
	self.table_info.attach(self.combobox_channels,1,2,0,1)
	self.table_info.attach(self.label_directions,0,1,1,2)
	self.table_info.attach(self.combobox_directions,1,2,1,2)
	self.table_info.attach(self.frame_volt,0,1,2,3)
	self.table_info.attach(self.label_volt,1,2,2,3)
	self.table_info.attach(self.frame_current,0,1,3,4)
	self.table_info.attach(self.label_current,1,2,3,4)
	self.table_info.attach(self.frame_w,0,1,4,5)
	self.table_info.attach(self.label_w,1,2,4,5)
	self.table_info.attach(self.frame_h,0,1,5,6)
	self.table_info.attach(self.label_h,1,2,5,6)
	self.table_info.attach(self.label_types,0,1,6,7)
	self.table_info.attach(self.combobox_types,1,2,6,7)

	self.hbox_scale_min = gtk.HBox(False, 0)
	self.hbox_scale_max = gtk.HBox(False, 0)
	self.label_scale_min = gtk.Label("Min: ")
	self.label_scale_max = gtk.Label("Max: ")
	self.button_open = gtk.Button("Open")
	self.adjustment_scale_min = gtk.Adjustment(0.0, 0.0, 101.0, 1.0, 5.0, 1.0)
	self.adjustment_scale_max = gtk.Adjustment(0.0, 0.0, 101.0, 1.0, 5.0, 1.0)
	self.scale_min = gtk.HScale(self.adjustment_scale_min)
	#self.scale_min.set_update_policy(gtk.UPDATE_CONTINUOUS)
	self.scale_min.set_digits(0)
	#self.scale_min.set_value_pos(gtk.POS_TOP)
	self.scale_min.set_draw_value(True)
	self.scale_max = gtk.HScale(self.adjustment_scale_max)
	self.scale_max.set_digits(0)
	#self.scale_max.set_update_policy(gtk.UPDATE_CONTINUOUS)
	self.button_save = gtk.Button("Save")
	self.button_quit = gtk.Button("Quit")
	self.table_process = gtk.Table(2, 2,True)
	self.togglebutton_level = gtk.ToggleButton("Level")
	self.togglebutton_flevel = gtk.ToggleButton("F-Level")
	self.togglebutton_cline = gtk.ToggleButton("C-Lines")
	self.table_process.attach(self.togglebutton_level,0,1,0,1)
	self.table_process.attach(self.togglebutton_flevel,1,2,0,1)
	self.table_process.attach(self.togglebutton_cline,0,1,1,2)
	self.hbox_scale_min.pack_start(self.label_scale_min,expand=False,fill=True,padding=0)
	self.hbox_scale_min.pack_end(self.scale_min,expand=True,fill=True,padding=0)
	self.hbox_scale_max.pack_start(self.label_scale_max,expand=False,fill=True,padding=0)
	self.hbox_scale_max.pack_end(self.scale_max,expand=True,fill=True,padding=0)
	self.vbox_ops.pack_start(self.table_info, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.hbox_scale_min, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.hbox_scale_max, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.table_process, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_end(self.button_quit, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_end(self.button_save, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_end(self.button_open, expand=False,fill=True,padding=0)
	################################ handling signals
	self.button_load.connect("clicked",self.select_path,None)
	self.combobox_files.connect('changed', self.update_all, None)
	self.combobox_channels.connect('changed', self.update_image, None)
	self.combobox_directions.connect('changed', self.update_image, None)
	self.button_open.connect('clicked', self.open_file, None)
	self.scale_min.connect('value_changed',self.update_image,None)
	self.scale_max.connect('value_changed',self.update_image,None)
	self.button_save.connect('clicked',self.save_file,None)
	self.togglebutton_level.connect('toggled',self.update_image,None)
	self.button_quit.connect('clicked',lambda w: gtk.main_quit())
	################################ Arrangement and show
	self.window.add(self.vbox_main)
	self.vbox_main.pack_start(self.hbox_files,expand=False,fill=True,padding=0)
	self.vbox_main.pack_start(self.hbox_main,expand=False,fill=True,padding=0)
	self.hbox_main.pack_start(self.view,expand=True,fill=True,padding=0)
	self.hbox_main.pack_end(self.vbox_ops,expand=True,fill=True,padding=0)
	self.window.show_all()
	
	
    def select_path(self, widget, data):
	# load image
	dialog = gtk.FileChooserDialog("Open..", self.window, 
	gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
	gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	#dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
	response = dialog.run()
	if response == gtk.RESPONSE_OK:
	    self.select_path = dialog.get_filename()
	    self.update_files()
	    print dialog.get_filename(), 'selected'
	elif response == gtk.RESPONSE_CANCEL:
	    #print 'Closed, no files selected'
	    pass
	dialog.destroy()
    
    def update_files(self):
	files = [f for f in os.listdir(self.select_path) if os.path.isfile(self.select_path +'/'+ f) and f[-3:] == 'sxm']
	model = self.combobox_files.get_model()
	if model:
	    model.clear()   
	if len(files) > 0:
	    model = self.combobox_files.get_model()
	    self.combobox_files.set_model(None)
	    files_sorted = sorted_ls(self.select_path, files) 
	    for item in files_sorted:
		#print item
		model.append([item])
	        #self.combobox_files.append_text(item)
	    self.combobox_files.set_model(model)
	    self.combobox_files.set_active(0)
	    self.combobox_files.grab_focus()
    
    def update_all(self,widget,data):
	active = self.combobox_files.get_active()
	model = self.combobox_files.get_model()
	if active < 0:
	    pass
	else:
	    #print  active
	    self.current_data = self.select_path +'/'+ model[active][0]
	    # change the image and change the image settings
	    self.load_new_data()
	    self.label_volt.set_text(self.bias +' '+ self.bu)
	    self.label_current.set_text(str(self.current) +' '+ self.cu)
	    self.label_w.set_text(str(self.xd) +' '+ self.xyu)
	    self.label_h.set_text(str(self.yd) +' '+ self.xyu)
	    model = self.combobox_channels.get_model()
	    self.combobox_channels.set_model(None)
	    model.clear()
	    for item in self.channels:
		model.append([item])
		#self.combobox_channels.append_text(item)
	    self.combobox_channels.set_model(model)
	    self.combobox_channels.set_active(self.channel_id)
	    self.update_image(widget,None)
	    self.adjustment_scale_min.set_value(0)
	    self.adjustment_scale_max.set_value(100)
	    #self.update_image(widget,None)
	    # change the combobox_channels
	    
    def update_image(self, widget, data):
	#print "update"
	gwy.gwy_app_data_browser_add(self.c)
	#self.load_new_data()
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
	self.local_c.set_double_by_name(self.data_id_str+"base/min", float(self.data_min + self.scale_min_current/100*self.data_dif))
	self.local_c.set_double_by_name(self.data_id_str+"base/max", float(self.data_min + self.scale_max_current/100*self.data_dif))
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
	self.combobox_files.grab_focus()
	gwy.gwy_app_data_browser_remove(self.c)
		    
	    
    def load_new_data(self):
	self.d_origin = None
	#gwy.gwy_app_data_browser_remove(self.c)
	self.c = gwy.gwy_file_load(self.current_data, gwy.RUN_NONINTERACTIVE)
	data_field_id = 0
	data_field = '/' + str(data_field_id) + '/data'
	self.d = self.c[data_field]
	meta_field = '/' + str(data_field_id) + '/meta'
	meta = self.c[meta_field]
	bias = meta['Bias']
	self.bias, self.bu = bias.split(' ')
	current = meta['Z controller Setpoint']
	current, cu = current.split(' ')
	self.current = float(current) * 1e12
	self.cu = 'pA'
	current_bias = 'pm'
	self.xd = self.d.get_xreal() * 1e9
	self.yd = self.d.get_yreal() * 1e9
	self.xyu = 'nm'
	# Setting the channels
	c_keys = self.c.keys_by_name()
	count = 0
	self.channels = []
	for item in c_keys:
	    if re.search(r'title',item):
		count = count + 1
	#print count
	self.channel_id = 0
	model = self.combobox_files.get_model()
	self.channel_str = model[self.channel_id][0]
	self.direction_id = 0
	for i in range(0,count,2):
	    title = '/' + str(i) + '/data/title'
	    temp_title = self.c[title]
	    temp_channel, temp_directions = temp_title.split(' ')
	    temp_directions = temp_directions[1:-1]
	    #print temp_directions, i
	    self.channels.append(temp_channel)
	#gwy.gwy_app_data_browser_remove(self.c)
    
    def load_data(self):
	self.channel_id = self.combobox_channels.get_active()
	model = self.combobox_channels.get_model()
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
	if self.togglebutton_level.get_active():
	    gwy.gwy_app_data_browser_select_data_field(self.c, 0)
	    gwy.gwy_process_func_run("level", self.c, gwy.RUN_IMMEDIATE)
	self.d = self.c[self.data_id_str + 'data']
	d_process = self.d.duplicate()
	self.data_min = self.d.get_min()
	self.data_max = self.d.get_max()
	self. data_dif = self.data_max - self.data_min
	self.scale_min_current = self.scale_min.get_value()
	self.scale_max_current = self.scale_max.get_value()
	bottom = self.data_min + self.scale_min_current/100*self.data_dif
	top = self.data_min + self.scale_max_current/100*self.data_dif
	d_process.clamp(bottom, top)
	#self.d.clamp(bottom, top)
	self.d = d_process
    
    def save_file(self,widget,data):
	save2png_text(self.current_data,'temp')
	self.combobox_files.grab_focus()
		
    def open_file(self,widget,data):
	gwy.gwy_app_file_load(self.current_data)
	
	
	
def main():
    gtk.main()
    return 0
	
if __name__ == "__main__":
    ImageBrowser()
    main()
