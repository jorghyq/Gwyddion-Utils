import pygtk
pygtk.require('2.0')
import gtk

data = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
#mask = gwy.gwy_app_data_browser_get_current(gwy.APP_MASK_FIELD)

# Just create a new full mask, not assuming the mask exists
#new_mask_data = data.new_alike(False)
#new_mask_data.add(1.0)
window = gtk.Window(gtk.WINDOW_TOPLEVEL)
# new_mask_data =  anotherfunction()

container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

gwy_container = gwy.gwy_app_settings_get()
data_container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
new_container = gwy.Container()
new_container.set_object_by_name("/0/data", data)


view = gwy.DataView(new_container)
view.set_data_prefix("/0/data")

layer = gwy.LayerBasic()
layer.set_data_key("/0/data")
layer.set_gradient_key("/0/base/palette")
layer.set_range_type_key("/0/base")
layer.set_min_max_key("/0/base")

view.set_base_layer(layer)
vbox = gtk.VBox(False,spacing=0)
button = gtk.Button("hi")
vbox.pack_start(button,expand=False)
hbox=gtk.HBox(False,spacing=0)
hbox.pack_start(view, expand=False, fill=False,padding=0)
hbox.pack_start(vbox, expand=False)
window.add(hbox)
button.show()
view.show()
vbox.show()
hbox.show()
window.show()
