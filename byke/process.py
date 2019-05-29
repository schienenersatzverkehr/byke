#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 17:26:47 2019

@author: MatzBook

HAPPY BIKE INDEX PROCESSOR

parameters:
    + cutoff frequency (in Hz)
    + window size (in seconds)
    + threshold  (in g)
    + 
    
"""


import os
import sys

import pandas as pd
import numpy as np

import json

#for determining the run time
import time

from PTpreprocess import *
from JSONtoolbox import *
from toolbox import *

if len(sys.argv) != 3:
    print "wrong amount of arguments"
    print len(sys.argv)
    sys.exit(1)

## highpass & RMN & Export different df

### global constants

gI = ('gFx','gFy','gFz')
I = ('ax','ay','az')
g = 9.81

# processing parameters
s = 2
t = 1.5
cutoff = 1.
order = 6


#import Tkinter
#import tkFileDialog
#
#Tkinter.Tk().withdraw() # Close the root window
#filename = tkFileDialog.askopenfilename()
#

#export_path = root + '/data/processed/citytracks/'
#
#def file_save():
#    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
#    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
#        return
#    text2save = str(text.get(1.0, END)) # starts from `1.0`, not `0.0`
#    f.write(text2save)
#    f.close()
#    
#filename = root + '/data/raw/citytracks/citytrack4.csv'

root = os.getcwd()

title = sys.argv[2]
filename = root + str(sys.argv[1])
if not os.path.isfile(filename):
    print 'File error'
    print filename
    print 'Is not a file'
    sys.exit(1)
export_path = root + '/data/processed/citytracks/'

print 'Importing...'
df = import_csv(path_dat = filename)
dat = first_process(df, drop_duplicates = 'true')

### HAPPY BIKE INDEX PROCESSOR

col = gI[2]

# check runtime
tic = time.clock()

# 1) dynamic thresholding
print 'Limit the input according to the threshold: ' + str(t) + '...'
dat = dyn_threshold(dat, col, t=t)

print 'get the sampling frequency:'
fs = round(getfN(dat[:5000]),2) #sampling freq
print str(fs) + ' Hz'


# 2) highpass me
print 'Highpass (%s Hz) filter the signal...' % str(cutoff)
colpass = 'bhp_%sHz' %str(cutoff)
passmehigh(dat, col, cutoff, fs, order)

# 3) floating root mean square
print 'Calculating Floating root mean square of filtered signal...'
colrmn = str(colpass) +'_rmn'
dat[colrmn] = floating_RMN(dat[colpass], int(s * fs), 2)

# 4) average of geotags
print 'Calculate average of Geotags...'
avg = average_geotags(dat, col = colrmn)

# 5) normalize
print 'Normalize the averages...'
colnorm = 'N_' + colrmn 
avg[colnorm] = normalize(avg[colrmn])

# 6) export to geoJSON
processed = df_geojson(df=avg, col = colnorm)

# opt 7) safe to file directory 
try:
    # make sure export path is delivered
    
    dat_js = processed
    output_filename = '%s_c%s_s%s_t%s.geojson' % (title, cutoff, s, t)
    with open(export_path + output_filename, 'wb') as output_file:
        output_file.write(json.dumps(dat_js))
except:
    print 'Failed to Export: Unknown Error'

toc = time.clock()
print 'Done!' 
print 'time: '
print toc-tic/10000