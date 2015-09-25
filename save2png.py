import gwy
import os
c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

filename = c['/filename']
dir_path,basename = os.path.split(filename)
basename = basename[0:-4]

print dir_path,base_name
d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
data_field_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
meta_field = '/' + str(data_field_id) + '/meta'
title = '/' + str(data_field_id) + '/data/title'
channel = c[title]
print channel
gwy.gwy_app_data_browser_select_data_field(c,data_field_id)
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
count = 1
output_name = basename+'_'+str(xd)+xyu+'_'+str(yd)+xyu+'_'+bias+bu+'_'+str(current)+cu+'_'+str(count)+'.png'
while os.path.exists(output_name):
    count = count + 1
    output_name = basename+'_'+str(xd)+xyu+'_'+str(yd)+xyu+'_'+bias+bu+'_'+str(current)+cu+'_'+str(count)+'.png'
output_path = os.path.join(dir_path,'temp')
if not os.path.isdir(output_path):
    os.mkdir(output_path)
output = os.path.join(output_path,output_name)
print output
#img.save(output)
gwy.gwy_file_save(c, output, gwy.RUN_NONINTERACTIVE) 