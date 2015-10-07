import gwy
import re
import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mlp
import numpy as np

def save2png_text(data_path, data, dist_dir = 'overview', log = 0):
# get the current container and datafield
    c = gwy.gwy_file_load(data_path, gwy.RUN_NONINTERACTIVE)
    data_field_id = 0
    data_field = '/' + str(data_field_id) + '/data'
    d = c[data_field]
    #gwy.gwy_process_func_run("facet-level", c, gwy.RUN_IMMEDIATE)
    #filename = c['/filename']
    dir_path,basename = os.path.split(data_path)

    meta_field = '/' + str(data_field_id) + '/meta'
    title = '/' + str(data_field_id) + '/data/title'
    channel = c[title]
    meta = c[meta_field]
    #basename = meta['File name']
    #basename = basename.split('\\')[-1]
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

    w = d.get_xres()
    h = d.get_yres()
    #data_field = '/' + str(data_field_id) + '/data'
    #array = gwyutils.data_field_data_as_array(d)
    #d.data_changed()
    
    array = np.array(data.get_data()).reshape(w,h)
    ############## DATA PROCESSING #################
    #data_temp = array.T
    #n = w
    #xi = np.arange(n)
    ##print xi
    #x= np.array([xi,np.ones(n)])
    #w_temp = np.linalg.lstsq(x.T,data_temp)[0]
    #data_sub = np.zeros([n,n])
    #X = np.array([xi,]*int(n)).T
    #Y = (X*w_temp[0]+w_temp[1]).T
    #array = array - Y
    #print array.shape
    ############# DATA PROCESSING END ##############
    
    #array = np.transpose(array)
    # set the rescaling
    #b_name = '/' + str(data_field_id) + '/base/'
    #range_type = '/' + str(data_field_id) + '/range-type'
    #c.set_string_by_name(range_type,'2')
    
    ##b_min = b_name + 'min'
    #b_max = b_name + 'max'
    #if c.contains_by_name(b_min) and c.contains_by_name(b_max):
        #pixel_min = c[b_min]
        #pixel_max = c[b_max]
        #CHANGE_COLOR_RANGE = 1
        #if CHANGE_COLOR_RANGE:
            #array[np.where(array < pixel_min)] = pixel_min
            #array[np.where(array > pixel_max)] = pixel_max
    high = 255
    low = 0
    amin = array.min()
    amax = array.max()
    rng = amax - amin
    array2 = high - (((high - low) * (amax - array)) / rng)
    new = np.zeros((w+50,h))
    new[:,:] = 255
    new[:w,:h] = array2
    new = new.astype('uint8')
    # load colormap
    palette_name = '/' + str(data_field_id) + '/base/palette'
    cm = 'gray' 
    #if c.contains_by_name(palette_name):
        #palette = c[palette_name]
        #if palette == "Julio":
            #fire = np.loadtxt('/home/jorghyq/.gwyddion/pygwy/fire.txt',delimiter=' ')
            #cm = mlp.colors.ListedColormap(fire/255)
    fire = np.loadtxt('/home/jorghyq/.gwyddion/pygwy/fire.txt',delimiter=' ')
    cm = mlp.colors.ListedColormap(fire/255)
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
    output_text = str(xd)+xyu+'_'+str(yd)+xyu+'_'+bias+bu+'_'+str(current)+cu+'_'+str(w)
    plt.text(5, w+25,basename,fontsize=16)
    plt.text(5, w+50,output_text,fontsize=16)
    output_path = os.path.join(dir_path,dist_dir)
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    count = 1
    output_name = basename + '_'+ch_out+'_'+ fb_ward+ '_' + str(count) + '.png'
    #while os.path.exists(os.path.join(output_path,output_name)):
    #    count = count + 1
    #    output_name = basename + '_'+ch_out+'_'+ fb_ward+ '_' + str(count) + '.png'
    output = os.path.join(output_path,output_name)
    plt.axis('off')
    plt.xticks([])
    plt.yticks([])
    #plt.imsave(output,new,cmap=cm)
    plt.savefig(output,cmap=cm,bbox_inches='tight', pad_inches=0,dpi=100)
    plt.close()

if __name__ == '__main__':
    sample_path = '/home/jorghyq/Project/GwyUtils/A150112.163633-01194.sxm'
    save2png_text(sample_path)