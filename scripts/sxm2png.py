import gwy
import re
import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mlp
import numpy as np
sys.path.insert(1, './scripts/')
from convert_sxm2png_text import save2png_text

ROOT = '/home/jorghyq/Project/GwyUtils/test/'
files = [f for f in os.listdir(ROOT) if os.path.isfile(ROOT + f) and f[-3:] == 'sxm']
#print files, len(files)

for data in files:
    data_path = ROOT + data
    save2png_text(data_path)
    print data_path,'is done'
    
