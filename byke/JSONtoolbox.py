#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 17:24:20 2019

@author: MatzBook
"""

import json
from geojson import Point, LineString, GeometryCollection, Feature, FeatureCollection


def df_geojson(df, col):
    
    """
    exporting arbitrary df to geoJSON
    
    df has to have Following format:
    
    col describes the source column
    its values have to be normalized between 0 and 1
    
    'az'%'ax'%'ay'%'Longitude'%'Latitude'
    
    """
    entries = []
    for i in range(0, len(df)):

        item = df.iloc[i]
        lng = str_to_float(item['Longitude'])
        lat = str_to_float(item['Latitude'])
        index = item[col]

        entry = {'lng': lng, 
                'lat': lat, 
                'index': index
                }

        entries.append(entry)

    ## Convert to GeoJSON
    features = []
    for i in range(0, len(entries)-2):
        x = entries [i]
        y = entries[i+1]
        line = LineString([(x['lng'], x['lat']), 
                           (y['lng'], y['lat'])])
        
        feature = Feature(geometry=line, properties={
            "index": x['index'],
            "stroke": index_to_color(x['index']),
            "stroke-width": 2,
            "stroke-opacity": 1
        })

        features.append(feature)

    _geojson = FeatureCollection(features)
    
    return _geojson

def df_to_geojson(df, export_path=None, lat_row='Latitude', lng_row='Longitude'):
    """ 
   
    Konvertiert das Dataframe der GPS Sensoraufnahme (GPS.csv) in GeoJSON (ohne Index-Berechnung). 
    """
    points = []
    for i in range(0, len(df)):
        x = df.iloc[i]
        p = Point(str_to_float(x[lng_row]), str_to_float(x[lat_row]))
        
        points.append(p)
    
    _geojson = GeometryCollection(points)
    
    if export_path:
        f = open (export_path, 'w')
        f.write(json.dumps(_geojson))
    return _geojson

def index_to_color(index):  
    """
    return color for value between 0 and 1 
    
    color gradient green, yellow, red 
    """
    color_gradient = [
            '#2bff00', '#74ff00', '#9eff00', '#bfff00', '#dcff00',
            '#ebef00', '#f7e000', '#ffd000', '#ffad00', '#ff8700',
            '#ff5b00', '#ff0000'
        ]
    i = index * len(color_gradient)
    i = int(round(i)) - 1
    if(i<=0):
        return color_gradient[0]
    return color_gradient[i]



# TODO make it str.replace()

def str_to_float(value):
    
    """ old gFone
    3,141 (str) --> 3.141 (float)
    """
    if isinstance(value, float) or isinstance(value, int):
        return float(value)
    else:
        return float(value.replace(',', '.'))

