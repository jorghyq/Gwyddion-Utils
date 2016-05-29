# This script convert the standalone SPMBrowser into a process module in
# Gwyddion

import os
import shutil
import re

local_src = 'gb-standalone/'
local_dst = 'pygwy/'
dst = '/home/jorghyq/.gwyddion/pygwy'


# convert the standalone program into module format
# copy the files from standalone directory to local pygwy directory
if os.path.isdir(local_dst):
    shutil.rmtree(local_dst)
    os.mkdir(local_dst)
for item in os.listdir(local_src):
    if item[-3:] == '.py':
        shutil.copy2(local_src+item, local_dst)
        print item, 'copied to', local_dst

# prepare the files for gwyddion module
shutil.move(local_dst+'SPMBrowser.py', local_dst+'image_browser.py')
with open(local_dst+'image_browser.py','r') as f:
    text = f.readlines()

# load the text for the module specification
with open('convert.txt','r') as f:
    temp_text = f.readlines()
    ind_split = temp_text.index('# part after the code\n')
    pre_text = temp_text[:ind_split]
    post_text = temp_text[ind_split:]
    #print pre_text
    #print post_text

with open(local_dst+'temp.txt','w') as f:
    for line in text:
        # if reach the pre-module sign
        if re.search(r'pre-module',line):
            for temp_line in pre_text:
                f.write(temp_line)
        if re.search(r'post-module',line):
            for temp_line in post_text:
                f.write(temp_line)
        f.write(line)

os.remove(local_dst+'image_browser.py')
shutil.move(local_dst+'temp.txt',local_dst+'image_browser.py')

# clean the .gwyddion directory

# copy the relavent files into .gwyddion directory
if os.path.isdir(dst):
    shutil.rmtree(dst)
    os.mkdir(dst)

for item in os.listdir(local_dst):
    if item[-3:] == '.py':
        shutil.copy2(local_dst+item, dst)
        print item, 'copied to', dst

