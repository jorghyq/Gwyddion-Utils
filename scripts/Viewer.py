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
from Navigator import Navigator
from Imager import Imager
from Infor import Infor
from Operator import Operator
from GwyData import GwyData

# Class for navigation
class SPMBrowser():
    def __init__(self):
        self.parent = parent
        # Definiton of the variables
        self.path_selected = None
        self.navi = Navigator()
        self.info = Infor()
        self.oper = Operator()
        self.gwydata = GwyData()
        self.img_1 = Imager()
        self.img_2 = Imager()
        # Definition of the widget
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.set_title("SPMBrowser")


