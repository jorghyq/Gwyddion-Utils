#!/usr/bin/env python
#import pygtk
#pygtk.require('2.0')
#import gtk
import sys
import os
sys.path.insert(1,"/usr/local/lib64/python2.7/site-packages")
import gwy
import re
import numpy as np
import matplotlib as mlp
import matplotlib.pyplot as plt

# format float to string
def f2s(input_float):
    return "{0:.1f}".format(input_float)

class GwyData():
    def __init__(self):
        self.c = None
        self.param = {}
        self.param['bias'] = 'NG'
        self.param['bu'] = 'V'
        self.param['current'] = 'NG'
        self.param['cu'] = 'nA'

    def load_data(self,data_path):
        self.current_data = data_path
        self.c = gwy.gwy_file_load(self.current_data,gwy.RUN_NONINTERACTIVE)
        data_field_id = 0
        data_field = '/' + str(data_field_id) + '/data'
        self.d = self.c[data_field]
        meta_field = '/' + str(data_field_id) + '/meta'
        meta = self.c[meta_field]
        if meta.contains_by_name('Bias'):
            bias = meta['Bias']
            self.param['bias'] = bias.split(' ')[0]
            self.param['bu'] = bias.split(' ')[-1]
        #print bias
        if self.c.contains_by_name('/meta/eepa/GapVoltageControl.Voltage'):
            self.param['bias'] = self.c['/meta/eepa/GapVoltageControl.Voltage']
        self.param['full_path'] = self.current_data
        if meta.contains_by_name('Z controller Setpoint'):
            current = meta['Z controller Setpoint']
            current, cu = current.split(' ')
            self.param['current'] = float(current) * 1e12
            self.param['cu'] = 'pA'
        if self.c.contains_by_name('/meta/eepa/Regulator.Setpoint_1'):
            self.param['current'] = self.c['/meta/eepa/Regulator.Setpoint_1']*1e9
        current_bias = 'pm'
        self.param['width'] = self.d.get_xreal() * 1e9
        self.param['height'] = self.d.get_yreal() * 1e9
        self.param['xyu'] = 'nm'
        self.param['w_dim'] = self.d.get_xres()
        self.param['h_dim'] = self.d.get_yres()
        # Setting the channels
        c_keys = self.c.keys_by_name()
        count = 0
        channels = []
        for item in c_keys:
            if re.search(r'title',item):
                count = count + 1
        #print count
        for i in range(0,count,2):
            title = '/' + str(i) + '/data/title'
            temp_title = self.c[title]
            if self.param['full_path'][-3:] == 'sxm':
                temp_channel, temp_directions = temp_title.split(' ')
                temp_directions = temp_directions[1:-1]
            elif self.param['full_path'][-6:] =='Z_mtrx':
                print temp_title, temp_title.strip().split(' ')
                temp_channel = temp_title.strip().split(' ')[-1]
                print temp_channel
            else:
                temp_channel = temp_title
            #print temp_directions, i
            channels.append(temp_channel)
        self.param['channels'] = channels

    def get_param(self):
        return self.param

    def get_container(self):
        return self.c

    def save2png(self,channel,cm_low=None,cm_high=None,dest_dir=None):
        if channel in self.param['channels']:
            data_field_id = self.param['channels'].index(channel)
            data_filed_id = data_field_id * 2
        else:
            data_field_id = 0
        data_field = '/' + str(data_field_id) + '/data'
        d = self.c[data_field]
        dir_path,basename = os.path.split(self.param['full_path'])
        # parameters
        bias = self.param['bias']
        bu = self.param['bu']
        current = self.param['current']
        cu = self.param['cu']
        xd = self.param['width']
        yd = self.param['height']
        xyu = self.param['xyu']
        w = self.param['w_dim']
        h = self.param['h_dim']
        # load the data
        array = np.array(d.get_data()).reshape(w,h)
        ############## DATA PROCESSING #################
        #data_temp = array.T
        #n = w
        #xi = np.arange(n)
        #print xi
        #x= np.array([xi,np.ones(n)])
        #w_temp = np.linalg.lstsq(x.T,data_temp)[0]
        #data_sub = np.zeros([n,n])
        #X = np.array([xi,]*int(n)).T
        #Y = (X*w_temp[0]+w_temp[1]).T
        #array = array - Y
        #print array.shape
        ############# DATA PROCESSING END ##############
        #b_name = '/' + str(data_field_id) + '/base/'
        #range_type = '/' + str(data_field_id) + '/range-type'
        #c.set_string_by_name(range_type,'2')
        #b_min = b_name + 'min'
        #b_max = b_name + 'max'
        #if c.contains_by_name(b_min) and c.contains_by_name(b_max):
        #    pixel_min = c[b_min]
        #    pixel_max = c[b_max]
        #    CHANGE_COLOR_RANGE = 1
        #    if CHANGE_COLOR_RANGE:
        #        array[np.where(array < pixel_min)] = pixel_min
        #        array[np.where(array > pixel_max)] = pixel_max
        high = 255
        low = 0
        amin = array.min()
        amax = array.max()
        rng = amax - amin
        array2 = high - (((high - low) * (amax - array)) / rng)
        if cm_low and cm_high:
            print cm_low,cm_high
            low = cm_low * 255 /100
            high = cm_high * 255 /100
            array2[np.where(array < low)] = low
            array2[np.where(array > high)] = high
        new = np.zeros((w+int(round(w*0.06)),h))
        new[:,:] = 255
        new[:w,:h] = array2
        new = new.astype('uint8')
        # load colormap
        ch_out = None
        match_df = re.search(r'Frequency_Shift',channel)
        match_c = re.search(r'Current',channel)
        match_z = re.search(r'Z',channel)
        #print channel
        cm = 'gray'
        fire = np.loadtxt('/home/jorghyq/.gwyddion/pygwy/fire.txt',delimiter=' ')
        if match_df:
            ch_out = 'df'
            cm = 'gray'
        elif match_c:
            ch_out = 'current'
            cm = mlp.colors.ListedColormap(fire/255)
        elif match_z:
            ch_out = 'z'
            cm = mlp.colors.ListedColormap(fire/255)
        output_text = f2s(xd)+xyu+'_'+f2s(yd)+xyu+'_'+bias+bu+'_'+f2s(current)+cu+'_'+str(w)+'_'+str(h)
        palette_name = '/' + str(data_field_id) + '/base/palette'
        #if c.contains_by_name(palette_name):
            #palette = c[palette_name]
            #if palette == "Julio":
                #fire = np.loadtxt('/home/jorghyq/.gwyddion/pygwy/fire.txt',delimiter=' ')
                #cm = mlp.colors.ListedColormap(fire/255)
        #cm = 'Gwyddion.net'
        img = plt.imshow(new, cmap = cm)
        # determine the channel
        plt.text(5, w+int(round(w*0.03)),basename,fontsize=12)
        plt.text(5, w+int(round(w*0.06)),output_text,fontsize=12)
        if dest_dir:
            output_path = dest_dir
        else:
            output_path = os.path.join(dir_path,'temp')
        print 'convert to',output_path
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        count = 1
        if ch_out:
            output_name = basename[:-4] + '_'+ch_out+'_'+ str(count) + '.png'
        else:
            output_name = basename[:-4] + '_'+ str(count) + '.png'
        #while os.path.exists(os.path.join(output_path,output_name)):
        #    count = count + 1
        #    output_name = basename + '_'+ch_out+'_'+ fb_ward+ '_' + str(count) + '.png'
        output = os.path.join(output_path,output_name)
        plt.axis('off')
        plt.xticks([])
        plt.yticks([])
        #plt.imsave(output,new,cmap=cm)
        plt.savefig(output,cmap=cm,bbox_inches='tight', pad_inches=0,dpi=300)
        plt.clf()



if __name__ == "__main__":
    gwydata =GwyData()
    gwydata.load_data('/home/jorghyq/Project/Gwyddion-Utils/test/A151117.155350-00742.sxm')
    print gwydata.param['channels']
