import gwy
import os

plugin_menu = "/Basic Operations/save2png"
plugin_type = "PROCESS"
plugin_desc = "save2png"

def run():
    c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
    filename = c['/filename']
    dir_path,basename = os.path.split(filename)
    basename = basename[0:-4]
    #print dir_path,base_name
    d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
    data_field_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
    meta_field = '/' + str(data_field_id) + '/meta'
    title = '/' + str(data_field_id) + '/data/title'
    channel = c[title]
    #print channel
    gwy.gwy_app_data_browser_select_data_field(c,data_field_id)
    #meta = c[meta_field]
    #print meta.keys_by_name()
    #bias = meta['Bias']
    #bias, bu = bias.split(' ')
    #current = meta['Z controller Setpoint']
    #current, cu = current.split(' ')
    #current = float(current) * 1e12
    #cu = 'pA'
    #current_bias = 'pm'
    #xd = d.get_xreal() * 1e9
    #yd = d.get_yreal() * 1e9
    #xyu = 'nm'
    output_path = dir_path
    output_name = basename + '.png'
    output = os.path.join(output_path,output_name)
    gwy.gwy_file_save(c, output, gwy.RUN_NONINTERACTIVE)
