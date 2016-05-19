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
temp_name = basename+'_temp.png'
gwy.gwy_file_save(c, temp_name, gwy.RUN_NONINTERACTIVE)

# prepare to save
w = d.get_xres()
h = d.get_yres()
io.use_plugin('freeimage')
data_field = '/' + str(data_field_id) + '/data'
img = Image.open(temp_name)
I = np.asarray(img)
print len(I.shape)
if len(I.shape) > 2:
    new = np.zeros((w+40,h,3))
    new[:,:,:] = 256
    new[:w,:h,:] = I
    new = new.astype('int16')
else:
    new = np.zeros((w+40,h))
    new[:,:] = 65535
    new[:w,:h] = I
    new = new.astype('int32')

img = Image.fromarray(new)


# determine the channel
ch_out = None
fb_ward = None
match_df = re.search(r'Frequency_Shift ',channel)
match_c = re.search(r'Current ',channel)
match_z = re.search(r'Z ',channel)
match_forward = re.search(r'(Forward)',channel)
match_backward = re.search(r'(Backward)',channel)
if match_df:
    ch_out = 'df'
if match_c:
    ch_out = 'current'
if match_z:
    ch_out = 'z'
    
if match_forward:
    fb_ward = 'F'
if match_backward:
    fb_ward = 'B'
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf",30)
#draw.rectangle([0,0,200,40],fill=65535)
output_text = str(xd)+xyu+'_'+str(yd)+xyu+'_'+bias+bu+'_'+str(current)+cu+'_'+str(w)+'_'+str(h)
draw.text((0, w),output_text,font=font,fill=0)
count = 1
output_name = basename + '_'+ch_out+'_'+ fb_ward+ '_' + str(count) + '.png'
while os.path.exists(output_name):
    count = count + 1
    output_name = basename + '_'+ch_out+'_'+ fb_ward+ '_' + str(count) + '.png'
img.save(output_name)
#os.remove(temp_name)
#io.imsave(basename+'test_16bit.png', np.transpose(-array2)) 