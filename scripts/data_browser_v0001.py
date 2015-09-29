data = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
mask = gwy.gwy_app_data_browser_get_current(gwy.APP_MASK_FIELD)

# Just create a new full mask, not assuming the mask exists
new_mask_data = data.new_alike(False)
new_mask_data.add(1.0)

# new_mask_data =  anotherfunction()

container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
# ???
#i = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
#container.set_object_by_name("/%d/mask" % i, new_mask_data)
 #new_mask_data.data_changed()

dialog = gtk.Dialog("Title",
                        None,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                         gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

gwy_container = gwy.gwy_app_settings_get()
data_container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
new_container = gwy.Container()
new_container.set_object_by_name("/0/data", data)

new_container.set_object_by_name("/0/mask", new_mask_data)

view = gwy.DataView(new_container)
# May not be necessary here but always better to do.
view.set_data_prefix("/0/data")

layer = gwy.LayerBasic()
    # Fixed data key
layer.set_data_key("/0/data")
layer.set_gradient_key("/0/base/palette")
layer.set_range_type_key("/0/base")
layer.set_min_max_key("/0/base")

view.set_base_layer(layer)

layer2 = gwy.LayerMask()
layer2.set_data_key("/0/mask")
layer2.set_color_key("/0/mask")
# Set the mask colour (can also copy it from the original data).
new_container['/0/mask/green'] = 1.0
new_container['/0/mask/alpha'] = 0.5

view.set_alpha_layer(layer2)

hbox=gtk.HBox(False,spacing=0)
hbox.pack_start(view, expand=True, fill=False,padding=0)
    # Actually show the data view.
dialog.vbox.pack_start(hbox, True, False, 0)

dialog.show_all()

response = dialog.run()
while response != gtk.RESPONSE_ACCEPT:
    if response == gtk.RESPONSE_REJECT or response == gtk.RESPONSE_DELETE_EVENT:
        break
    response = dialog.run()
dialog.destroy()