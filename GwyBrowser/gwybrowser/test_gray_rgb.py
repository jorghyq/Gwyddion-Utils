import gwy
import gwyutils
import re
import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import numpy as np
from skimage import io, exposure, img_as_uint, img_as_float
# get the current container and datafield
c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
data_field_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
gwy.gwy_app_data_browser_select_data_field(c,data_field_id)
filename = c['/filename']
basename = filename[0:-4]
print filename.split('/')[-1][:-4]

meta_field = '/' + str(data_field_id) + '/meta'
title = '/' + str(data_field_id) + '/data/title'
channel = c[title]
print channel

meta = c[meta_field]
print meta.keys_by_name()
bias = meta['Bias']
bias, bu = bias.split(' ')
current = meta['Z controller Setpoint']
current, cu = current.split(' ')
current = float(current) * 1e12
cu = 'pA'
current_bias = 'pm'
xd = d.get_xreal() * 1e9
yd = d.get_yreal() * 1e9
xyu = 'nm'
print xd
print bias
#gwy.gwy_file_save(c, basename+'_'+str(xd)+xyu+'_'+str(yd)+xyu+'_'+bias+bu+'_'+str(current)+cu+'.png', gwy.RUN_NONINTERACTIVE)

# prepare to save
w = d.get_xres()
h = d.get_yres()
io.use_plugin('freeimage')
data_field = '/' + str(data_field_id) + '/data'
array = gwyutils.data_field_data_as_array(d)
print array.shape