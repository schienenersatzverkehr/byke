#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 16:35:43 2019

@author: matthias franz-josef roetzer
"""

import pandas as pd
import numpy as np

def first_process(df_, drop_duplicates = 'true'):
    r"""
    in: dataframe with format: -time-ax-ay-az-latitude-longitude
    
        1. format (az,ax,ay) or (gFx, gFz, gFy) as float 
        2. format time column as pandas timestamp
        3. drop for all, timestamp or no duplicates (keep the last value)
    
    :returns 'cleaned' data table, 
        formated (acceleration values, timestamped),
        if desired, cleaned for duplicates 
    """
    
    df_dat = df_
    
    # speed
    if 'Speed (m/s)' in df_dat.columns:
        df_dat.loc[:,'velocity'] = df_dat['Speed (m/s)'].str.replace(",",".").astype(float)
        df_dat = df_dat.drop(columns='Speed (m/s)')
    
    # timestamps
    if 'time' in df_dat.columns:
        df_dat.loc[:,'time'] = pd.to_datetime(df_dat['time'], format = '%H:%M:%S:%f')
        
    if 'Unnamed: 7' in df_dat.columns:
        df_dat = df_dat.drop(columns = 'Unnamed: 7')
    
    # drop last to avoid data loss
    
    # TODO: add loop over I[]
    # linear acceleration
    if 'az' and 'ay' and 'ax' in df_dat.columns:
        if not df_dat['az'].dtypes == np.dtype('float64'):
            df_dat['az'] = df_dat['az'].str.replace(",",".").astype(float)
            df_dat['ay'] = df_dat['ay'].str.replace(",",".").astype(float)
            df_dat['ax'] = df_dat['ax'].str.replace(",",".").astype(float)

        if(drop_duplicates == 'true'):
            df_dat = dropfora(df_dat)
        elif(drop_duplicates == 'time'):
            df_dat = df_dat.drop_duplicates(['Latitude','Longitude','az', 'ay', 'ax'], keep = 'last')
    
    # TODO: add loop over gI[]
    # g-force
    if 'gFz' and 'gFy' and 'gFx' in df_dat.columns:
        if not df_dat['gFz'].dtypes == np.dtype('float64'):
            df_dat['gFz'] = df_dat['gFz'].str.replace(",",".").astype(float)
            df_dat['gFy'] = df_dat['gFy'].str.replace(",",".").astype(float)
            df_dat['gFx'] = df_dat['gFx'].str.replace(",",".").astype(float)

        if(drop_duplicates == 'true'):
            df_dat = dropforg(df_dat)
        elif(drop_duplicates == 'time'):
            df_dat = df_dat.drop_duplicates(['Latitude','Longitude','gFz', 'gFy', 'gFx'], keep = 'last')

    df_dat = df_dat.reset_index(drop=False)
    
    return df_dat 

def dropforg(df):
    return df.drop_duplicates(['gFx','gFy','gFz'], keep='last')

def dropfora(df):
    return df.drop_duplicates(['az','ax','ay'], keep='last')

def dropforspeedzero(df_):
    return df_.loc[df_['velocity'] > 0]

def set_same(x,y):
    """sets two arrays to the same size"""
    shp = min(len(x),len(y))
    return x[:shp],y[:shp]

def dropGeotags(data):
    """ dropping duplicate geotags"""
    len_before = len(data)
    data_dupl = data.drop_duplicates(['Latitude', 'Longitude'], keep = 'last')
    data_dupl = data_dupl.reset_index(drop = 'last')
    
    dropped = len_before - len(data_dupl)
    print "%d duplicates dropped" % dropped
    
    return data_dupl

def import_csv(path_dat):
    try:
        df_dat = pd.read_csv(path_dat, delimiter = ';')
        return df_dat
    except:
        print "import error"

def str_to_float(value):
    
    """ old gFone
    3,141 (str) --> 3.141 (float)
    """
    if isinstance(value, float) or isinstance(value, int):
        return float(value)
    else:
        return float(value.replace(',', '.')) 
