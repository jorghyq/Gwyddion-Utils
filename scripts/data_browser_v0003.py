#!/usr/bin/env python
# Image Browser for Gwyddion

import pygtk
pygtk.require('2.0')
import gtk
import sys
sys.path.insert(1,'/usr/local/lib64/python2.7/site-packages')
import gwy
import os
import numpy as np
import re
import matplotlib
matplotlib.use('GTK')
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from convert_sxm2png_text import save2png_text
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

# or NavigationToolbar for classic
#from matplotlib.backends.backend_gtk import NavigationToolbar2GTK as NavigationToolbar
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


def sorted_ls(path, files):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(files, key=mtime))

def rescale(array, high, low):
    amin = array.min()
    amax = array.max()
    rng = amax - amin
    if rng < 1e-10:
	output = np.zeros(array.shape)
    else:
	output = high - (((high - low) * (amax - array)) / rng)
	output = output.astype('uint8')
    return output

class ImageBrowser:
    def __init__(self):
	########### Initialize some variables ##############
	self.CHANNEL = None
	self.DIRECTION = None
	# load cmap
	self.fire = np.loadtxt('/home/jorghyq/.gwyddion/pygwy/fire.txt',delimiter=' ')
	self.fire_cm = matplotlib.colors.ListedColormap(self.fire/255)
	self.gradient_key = self.fire_cm
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
	self.fig = Figure(figsize=(5,4), tight_layout=True, dpi=100)
	self.ax = self.fig.add_subplot(111)
	self.ax.axis('off')
	self.ax.set_xticks([])
	self.ax.set_yticks([])
	self.ax.imshow(np.array([[2,4,5,5],[5,6,7,8],[7,6,5,7]]))
	self.canvas = FigureCanvas(self.fig)
	self.canvas.set_size_request(600, 600)
	#self.view = gwy.DataView(self.local_c)
	#self.hbox_image = gtk.HBox(False, 0)
	#self.hbox_image.set_size_request(400, 400)
	#self.view.set_size_request(400, 400)
	#self.hbox_image.set_usize(400, 400)
	#self.hbox_image.pack_start(self.view,expand=True,fill=True,padding=0)
	#self.hbox_image.set_bord(50)
	# vbox holding labels and operations
	self.vbox_ops = gtk.VBox(False,0)
	#self.vbox_ops.set_border_width(50)
	######################### elements for vbox_ops
	self.combobox_channels = gtk.combo_box_new_text()
	self.combobox_directions = gtk.combo_box_new_text()
	self.combobox_directions.append_text("Forward")
	self.combobox_directions.append_text("Backward")
	self.combobox_directions.set_active(0)
	self.label_channels = gtk.Label("Channel: ")
	self.label_directions = gtk.Label("Direction: ")
	self.label_volt = gtk.Label("V: ")
	self.label_current = gtk.Label("I: ")
	self.hbox_channels = gtk.HBox(False, 0)
	self.hbox_directions = gtk.HBox(False, 0)
	self.hbox_types = gtk.HBox(False, 0)
	self.hbox_scale_min = gtk.HBox(False, 0)
	self.hbox_scale_max = gtk.HBox(False, 0)
	self.label_w = gtk.Label("W: ")
	self.label_h = gtk.Label("H: ")
	self.label_types =gtk.Label("Type: ")
	self.combobox_types =gtk.combo_box_new_text()
	self.label_scale_min = gtk.Label("Min: ")
	self.label_scale_max = gtk.Label("Max: ")
	types = ["Unknown","Metal","Molecules","Useless"]
	for item in types:
	    self.combobox_types.append_text(item)
	    self.combobox_types.set_active(0)
	self.button_open = gtk.Button("Open")
	self.adjustment_scale_min = gtk.Adjustment(0.0, 0.0, 256.0, 1.0, 50.0, 2.0)
	self.adjustment_scale_max = gtk.Adjustment(0.0, 0.0, 256.0, 1.0, 50.0, 2.0)
	self.scale_min = gtk.HScale(self.adjustment_scale_min)
	self.scale_min.set_update_policy(gtk.UPDATE_CONTINUOUS)
	self.scale_min.set_digits(0)
	#self.scale_min.set_value_pos(gtk.POS_TOP)
	self.scale_min.set_draw_value(True)
	self.scale_max = gtk.HScale(self.adjustment_scale_max)
	self.scale_max.set_digits(0)
	self.button_save = gtk.Button("Save")
	self.scale_max.set_update_policy(gtk.UPDATE_CONTINUOUS)
	self.hbox_channels.pack_start(self.label_channels,expand=False,fill=True,padding=0)
	self.hbox_channels.pack_start(self.combobox_channels,expand=False,fill=True,padding=0)
	self.hbox_directions.pack_start(self.label_directions,expand=False,fill=True,padding=0)
	self.hbox_directions.pack_start(self.combobox_directions,expand=False,fill=True,padding=0)
	self.hbox_types.pack_start(self.label_types,expand=False,fill=True,padding=0)
	self.hbox_types.pack_start(self.combobox_types,expand=False,fill=True,padding=0)
	self.hbox_scale_min.pack_start(self.label_scale_min,expand=False,fill=True,padding=0)
	self.hbox_scale_min.pack_end(self.scale_min,expand=True,fill=True,padding=0)
	self.hbox_scale_max.pack_start(self.label_scale_max,expand=False,fill=True,padding=0)
	self.hbox_scale_max.pack_end(self.scale_max,expand=True,fill=True,padding=0)
	self.vbox_ops.pack_start(self.hbox_channels, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.hbox_directions, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.label_volt, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.label_current, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.label_w, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.label_h, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.hbox_types, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.button_open, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.hbox_scale_min, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.hbox_scale_max, expand=False,fill=True,padding=0)
	self.vbox_ops.pack_start(self.button_save, expand=False,fill=True,padding=0)
	#self.combobox_channels.show()
	#self.combobox_directions.show()
	#self.combobox_types.show()
	#self.label_channels.show()
	#self.label_directions.show()
	#self.label_types.show()
	#self.hbox_channels.show()
	#self.hbox_directions.show()
	#self.hbox_types.show()
	#self.label_volt.show()
	#self.label_current.show()
	#self.label_w.show()
	#self.label_h.show()
	#self.button_open.show()
	#self.scale_min.show()
	#self.scale_max.show()
	#self.label_scale_min.show()
	#self.label_scale_max.show()
	#self.hbox_scale_min.show()
	#self.hbox_scale_max.show()
	################################ handling signals
	self.button_load.connect("clicked",self.select_path,None)
	self.combobox_files.connect('changed', self.update_all, None)
	self.combobox_channels.connect('changed', self.update_image, None)
	self.combobox_directions.connect('changed', self.update_image, None)
	self.button_open.connect('clicked', self.open_file, None)
	self.scale_min.connect('value_changed',self.update_view,self.gradient_key)
	self.scale_max.connect('value_changed',self.update_view,self.gradient_key)
	self.button_save.connect('clicked',self.save_file,None)
	################################ Arrangement and show
	self.window.add(self.vbox_main)
	self.vbox_main.pack_start(self.hbox_files,expand=False,fill=True,padding=0)
	self.vbox_main.pack_start(self.hbox_main,expand=False,fill=True,padding=0)
	self.hbox_main.pack_start(self.canvas,expand=True,fill=True,padding=0)
	self.hbox_main.pack_end(self.vbox_ops,expand=True,fill=True,padding=0)
	#self.canvas.show()
	#self.vbox_ops.show()
	#self.combobox_files.show()
	#self.button_load.show()
	#self.hbox_files.show()
	#self.hbox_main.show()
	#self.vbox_main.show()
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
	    self.load_new_data(self.current_data)
	    self.label_volt.set_text("V: "+ self.bias +' '+ self.bu)
	    self.label_current.set_text("I: "+ str(self.current) +' '+ self.cu)
	    self.label_w.set_text("W: "+ str(self.xd) +' '+ self.xyu)
	    self.label_h.set_text("H: "+ str(self.yd) +' '+ self.xyu)
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
	    self.adjustment_scale_max.set_value(256)
	    # change the combobox_channels

    def update_image(self, widget, data):
	self.load_data()
	self.gradient_key = self.fire_cm
	#self.local_c.set_object_by_name(self.data_id_str+"data", self.d)
	if re.search(r'Z', self.channel_str):
	    #print self.channel_str
	    self.gradient_key = self.fire_cm
	elif re.search(r'Frequency', self.channel_str):
	    self.gradient_key = 'gray'
	self.update_view(widget,self.gradient_key)


    def load_new_data(self, data_path):
	self.c = gwy.gwy_file_load(data_path, gwy.RUN_NONINTERACTIVE)
	data_field_id = 0
	data_field = '/' + str(data_field_id) + '/data'
	self.d = self.c[data_field]
	meta_field = '/' + str(data_field_id) + '/meta'
	#title = '/' + str(data_field_id) + '/data/title'
	#self.channel = self.c[title]
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
	self.w = self.d.get_xres()
	self.h = self.d.get_yres()
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

    def load_data(self):
	self.channel_id = self.combobox_channels.get_active()
	model = self.combobox_channels.get_model()
	self.channel_str = model[self.channel_id][0]
	#print self.channel_str
	self.direction_id = self.combobox_directions.get_active()
	data_id = self.channel_id * 2 + self.direction_id
	#print self.channel_id,self.direction_id, data_id
	self.data_id_str = '/'+str(data_id)+'/'
	self.d = self.c[self.data_id_str + 'data']
	array = np.array(self.d.get_data())
	data_temp = rescale(array,255,0)
	self.data = data_temp.reshape(self.w,self.h)

    def update_view(self, widget, cm):
	self.scale_min_current = self.scale_min.get_value()
	self.scale_max_current = self.scale_max.get_value()
	self.ax.imshow(self.data,cmap=cm,vmin = self.scale_min_current, vmax = self.scale_max_current)


	self.canvas.draw()
	#print 'update view'

    def save_file(self,widget,data):
	#save2png_text(self.current_data)
	save_name = self.select_path + '/temp/' + os.path.basename(self.current_data)[:-3]+'png'
	print save_name
	self.fig.savefig(save_name,cmap=self.gradient_key,bbox_inches='tight', pad_inches=0,dpi=100)
	self.combobox_files.grab_focus()

    def open_file(self,widget,data):
	gwy.gwy_app_file_load(self.current_data)



def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ImageBrowser()
    main()
