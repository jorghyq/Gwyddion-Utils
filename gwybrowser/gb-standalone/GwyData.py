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
#from convert_sxm2png_text import save2png_text

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
        self.param['im_1_channel'] = 0
        self.param['im_2_channel'] = 0
        # for post-calibration
        self.param['ratio'] = 1

    def load_data(self,data_path):
        self.current_data = data_path
        self.param['full_path'] = self.current_data
        self.c = gwy.gwy_file_load(self.current_data,gwy.RUN_NONINTERACTIVE)
        data_field_id = 0
        data_field = '/' + str(data_field_id) + '/data'
        self.d = self.c[data_field]
        meta_field = '/' + str(data_field_id) + '/meta'
        meta = self.c[meta_field]
        # Extract bias and current, if needed
        ################ For Nanonis sxm file ################
        if meta.contains_by_name('Bias'):
            bias = meta['Bias']
            self.param['bias'] = bias.split(' ')[0]
            self.param['bu'] = bias.split(' ')[-1]
        if meta.contains_by_name('Z controller Setpoint'):
            current = meta['Z controller Setpoint']
            current, cu = current.split(' ')
            self.param['current'] = float(current) * 1e12
            self.param['cu'] = 'pA'
        ################ For Createc file ##################
        if meta.contains_by_name('Biasvolt[mV]'):
            self.param['bias'] = meta['Biasvolt[mV]']
            self.param['bu'] = 'mV'
        if meta.contains_by_name('Current[A]'):
            self.param['current'] = float(meta['Current[A]']) * 1e12
            self.param['cu'] = 'pA'
        ############### For Omicron file ###################
        if self.c.contains_by_name('/meta/eepa/GapVoltageControl.Voltage'):
            self.param['bias'] = self.c['/meta/eepa/GapVoltageControl.Voltage']
        if self.c.contains_by_name('/meta/eepa/Regulator.Setpoint_1'):
            self.param['current'] = self.c['/meta/eepa/Regulator.Setpoint_1']*1e9
        #current_bias = 'pm'
        ##### IF WANT TO SUPPORT MORE FORMATS, ADD PROCESSING CODE HERE #####
        self.param['width'] = self.d.get_xreal() * 1e9
        self.param['height'] = self.d.get_yreal() * 1e9
        self.param['width_real'] = self.param['width'] * self.param['ratio']
        self.param['height_real'] = self.param['height'] * self.param['ratio']
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
        print count
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

    #def save2png(self,channel,cm_low=None,cm_high=None,dest_dir=None):
    #   save2png_text(self.c,self.param,channel)


if __name__ == "__main__":
    gwydata =GwyData()
    gwydata.load_data('/home/jorghyq/Project/Gwyddion-Utils/test/F160730.003926.R.dat')
    print gwydata.param['channels']
