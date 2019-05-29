#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 17:41:21 2019

@author: MatzBook

TOOLBOX

processing tools

"""

import numpy as np
import pandas as pd
    
from scipy.signal import butter, lfilter


def normalize(data, thres = 0):
    """
    takes pandas.Series
    any x->(0,1)
    
    """
    
    min_data = min(data)
    maxi_data = max(data)
    
    if thres == 0:
        reach = (maxi_data - min_data)
    else:
        reach = (thres - min_data)

    normalize = pd.Series(data)
    
    for key, val in data.iteritems():
        normalize[key] = (val - min_data)/ reach
        
    return normalize

def rms(series):
    r"""
    Root Mean Square
    
    aka variance for _stationary_(?) data with zero as gravitational point
    
    :in pandas Series
    :returns rms as a float
    """
    _arr = series
    ms = 0    
    T = len(_arr)
    for i in range(T):
        k = _arr.iloc[i]
        # check if NaN
        if(k == k):
            ms = ms + k**2
        
    ms = ms/T
    
    return np.sqrt(ms)

def floating_RMN(df_col, w_size, N):
    r""" 
    Nth root-mean with certain kernel size
    *using convoltion*
    :in
    + column
    + window size
    + which N-th root mean
    
    :returns 'smoothed' signal """
    window = np.ones(w_size)/float(w_size)
    
    #rms = 'rms_' + str(size)
    
    df_col = np.power(df_col, N)
    dat = (np.convolve(df_col, window, 'same'))**(1./N)
    return dat

def thres(df_col, t):
    df_r = df_col
    df_r.loc[df_r > t] = t
    return df_r

def dyn_threshold(df_, col, t = 1.5, s=5):
    
    r""" dynamicaly sets the threshold for g force data
    + df_ : dataframe with gFi
    + t : relative to this threshold to be determined 
    + s : seconds of measure 
    
    """
    dat = df_
    
    t = 1.5 # g thres
    fn = getfN(dat[0:5000]) # observed size to 5000 :TODO
    w_s = s * fn 
    
    
    name_ = col + '_col_t'
    mean_ = rms(dat[col])
    
    dat_mean = dat[col].rolling(w_s, win_type = 'boxcar').mean()
    dat_mean = dat_mean.replace(np.NaN, mean_)
    
    dat[name_] = dat[col]
    dat[name_].loc[dat[col] > (dat_mean + t)] = dat_mean + t
    dat[name_].loc[dat[name_] < (dat_mean - t)] = dat_mean - t
    
    return dat

def average_geotags(data, col = 'azg'):
    
    """
    :in pandas DataFrame with 
            - geotags 'Latitude' and 'Longitude' 
            - positive acceleration data 'az' (HBI)
    
    :TODO make it euclidean ( -> sqrt(N^2))
    
    :returns geotags with moving average of the z-acceleration(az)
    
    """
    df = data
    
    #check for zeros 
    # Latitude & Longitude are dtype 'O' (object)...
    df = df[df['Latitude'] != '0,00000000']
    df = df.reset_index(drop = 1)
    
    df_geotags = pd.DataFrame(columns = [col, 'Latitude', 'Longitude'])
    i = 0
    k = 0

    lat = df['Latitude'].iloc[0]
    lon = df['Longitude'].iloc[0]

    sum1 = 0

    while(i < df.shape[0]-1):
        if(lat == df['Latitude'].iloc[i+1] and lon == df['Longitude'].iloc[i+1]):
            sum1 += df[col].iloc[i]
            k += 1
            i += 1
        else:
            avg = sum1/k
            df_geotags.loc[i] = [avg, lat, lon]
            k = 0
            sum1 = 0
            i += 1
            lat = df['Latitude'].iloc[i]
            lon = df['Longitude'].iloc[i]
            
    return df_geotags

def getfN(df_):
    """
    make sure stamp is 'time'
    
    just take a sample size of the dataframe not all
    
    returns sampling rate f_n in 1/s
    derived from sampling distance T, where T = 1/f_n
    """
    
    try:
        df_ = df_.reset_index()
    except:
        print 'already reindexed'
    
    delta = []
    
    for i in range(len(df_)-1):
        d =  df_.loc[i+1]['time'] - df_.loc[i]['time']
        delta = np.append(delta, d.total_seconds())
    
    return int(round(1/delta.mean()))

# BUTTERWORTH FILTERS


def highpass_butter(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = highpass_butter(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def passmehigh(dat, col, cutoff, fs, order):
    _ = 'bhp_%sHz' %str(cutoff) # column name
    dat[_] = butter_highpass_filter(dat[col], cutoff, fs, order)
