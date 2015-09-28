import gwy
import re
import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mlp
import numpy as np

plugin_menu = "/Basic Operations/Save2pngText"
plugin_type = "PROCESS"
plugin_desc = "save to png with text"

def run():
# get the current container and datafield
    c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
    d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
    data_field_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
    gwy.gwy_app_data_browser_select_data_field(c,data_field_id)
    filename = c['/filename']
    dir_path,basename = os.path.split(filename)

    basename = basename[0:-4]
    meta_field = '/' + str(data_field_id) + '/meta'
    title = '/' + str(data_field_id) + '/data/title'
    channel = c[title]
    meta = c[meta_field]
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

# prepare to save
    w = d.get_xres()
    h = d.get_yres()
    #io.use_plugin('freeimage')
    data_field = '/' + str(data_field_id) + '/data'
    #array = gwyutils.data_field_data_as_array(d)
    #d.data_changed()
    array = np.array(d.get_data()).reshape(w,h)
    #array = np.transpose(array)
    # set the rescaling
    b_name = '/' + str(data_field_id) + '/base/'
    b_min = b_name + 'min'
    b_max = b_name + 'max'
    if c.contains_by_name(b_min) and c.contains_by_name(b_max):
        pixel_min = c[b_min]
        pixel_max = c[b_max]
        CHANGE_COLOR_RANGE = 1
        if CHANGE_COLOR_RANGE:
            array[np.where(array < pixel_min)] = pixel_min
            array[np.where(array > pixel_max)] = pixel_max
    high = 255
    low = 0
    amin = array.min()
    amax = array.max()
    rng = amax - amin
    array2 = high - (((high - low) * (amax - array)) / rng)
    new = np.zeros((w+25,h))
    new[:,:] = 255
    new[:w,:h] = array2
    new = new.astype('uint8')
    # load colormap
    palette_name = '/' + str(data_field_id) + '/base/palette'
    cm = 'gray' 
    if c.contains_by_name(palette_name):
        palette = c[palette_name]
        if palette == "Julio":
            fire = np.loadtxt('/home/jorghyq/.gwyddion/pygwy/fire.txt',delimiter=' ')
            cm = mlp.colors.ListedColormap(fire/255)
    #    else:
    #        cm = 'gray'
    #else:    
    #    cm = 'gray'
    img = plt.imshow(new, cmap = cm)
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
    output_text = basename+'.sxm'+': '+str(xd)+xyu+'_'+str(yd)+xyu+'_'+bias+bu+'_'+str(current)+cu+'_'+str(w)+'_'+str(h)
    plt.text(5, w+13,output_text,fontsize=8)
    output_path = os.path.join(dir_path,'temp')
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    count = 1
    output_name = basename + '_'+ch_out+'_'+ fb_ward+ '_' + str(count) + '.png'
    while os.path.exists(os.path.join(output_path,output_name)):
        count = count + 1
        output_name = basename + '_'+ch_out+'_'+ fb_ward+ '_' + str(count) + '.png'
    output = os.path.join(output_path,output_name)
    plt.axis('off')
    plt.savefig(output,cmap=cm)
    plt.close()
