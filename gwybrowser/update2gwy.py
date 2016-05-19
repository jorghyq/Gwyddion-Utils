# This script convert the standalone SPMBrowser into a process module in
# Gwyddion

import os
import shutil

local_src = 'gwybrowser/'
local_dst = 'pygwy/'
dst = '~/.gwyddion'


# convert the standalone program into module format
for item in os.listdir(local_src):
    if item[-3:] == '.py':
        shutil.copy2(local_src+item, local_dst)
        print item, 'copied to', local_dst

shutil.move(local_dst+'SPMBrowser.py', local_dst+'image_browser.py')

# copy the relavent files into .gwyddion directory
