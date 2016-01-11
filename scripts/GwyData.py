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

class GwyData():
    def __init__(self):
        self.c = None
        self.param = {}

    def load_data(self,data_path):
        self.current_data = data_path
        #print self.current_data
        self.c = gwy.gwy_file_load(self.current_data,gwy.RUN_NONINTERACTIVE)
        data_field_id = 0
        data_field = '/' + str(data_field_id) + '/data'
        self.d = self.c[data_field]
        meta_field = '/' + str(data_field_id) + '/meta'
        meta = self.c[meta_field]
        bias = meta['Bias']
        print bias
        self.param['bias'] = bias.split(' ')[0]
        self.param['bu'] = bias.split(' ')[-1]
        current = meta['Z controller Setpoint']
        current, cu = current.split(' ')
        self.param['current'] = float(current) * 1e12
        self.param['cu'] = 'pA'
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
            temp_channel, temp_directions = temp_title.split(' ')
            temp_directions = temp_directions[1:-1]
            #print temp_directions, i
            channels.append(temp_channel)
        self.param['channels'] = channels

        def get_param(self):
            return self.param

        def get_container(self):
            return self.c


if __name__ == "__main__":
    gwydata =GwyData()
    gwydata.load_data('/home/jorghyq/Project/Gwyddion-Utils/A151201.000102-01691.sxm')
    print gwydata.param['channels']
