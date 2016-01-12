import re
import os
import sys
sys.path.insert(1,'/usr/local/lib64/python2.7/site-packages')
import matplotlib.pyplot as plt
import gwy
from GwyData import GwyData
import matplotlib as mlp
import numpy as np

# format float to string
def ffs(input_float):
    return "{0:.1f}".format(input_float)

def save2png_text(container,param, dest_dir=None, channel='Z'):
    c = container
    param = param
    channels = param['channels']
    if channel in channels:
        data_field_id = channels.index(channel)
    else:
        data_field_id = 0
    data_field = '/' + str(data_field_id) + '/data'
    d = c[data_field]
    dir_path,basename = os.path.split(param['full_path'])
    # parameters
    bias = param['bias']
    bu = param['bu']
    current = param['current']
    cu = param['cu']
    xd = param['width']
    yd = param['height']
    xyu = param['xyu']
    w = param['w_dim']
    h = param['h_dim']
    data_field = '/' + str(data_field_id) + '/data'
    # load the data
    array = np.array(d.get_data()).reshape(w,h)
    ############## DATA PROCESSING #################
    data_temp = array.T
    n = w
    xi = np.arange(n)
    #print xi
    x= np.array([xi,np.ones(n)])
    w_temp = np.linalg.lstsq(x.T,data_temp)[0]
    data_sub = np.zeros([n,n])
    X = np.array([xi,]*int(n)).T
    Y = (X*w_temp[0]+w_temp[1]).T
    array = array - Y
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
    new = np.zeros((w+int(round(w*0.06)),h))
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
    #fire = np.loadtxt('/home/jorghyq/.gwyddion/pygwy/fire.txt',delimiter=' ')
    #cm = mlp.colors.ListedColormap(fire/255)
    #cm = 'Gwyddion.net'
    img = plt.imshow(new, cmap = cm)
    # determine the channel
    ch_out = None
    match_df = re.search(r'Frequency_Shift',channel)
    match_c = re.search(r'Current',channel)
    match_z = re.search(r'Z',channel)
    if match_df:
        ch_out = 'df'
    if match_c:
        ch_out = 'current'
    if match_z:
        ch_out = 'z'
    output_text = ffs(xd)+xyu+'_'+ffs(yd)+xyu+'_'+bias+bu+'_'+ffs(current)+cu+'_'+str(w)+'_'+str(h)
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
    output_name = basename[:-4] + '_'+ch_out+'_'+ str(count) + '.png'
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

if __name__ == '__main__':
    gwydata = GwyData()
    gwydata.load_data('/home/jorghyq/Project/Gwyddion-Utils/test/A151117.155350-00742.sxm')
    save2png_text(gwydata)
    print gwydata.param['w_dim'],gwydata.param['h_dim']
