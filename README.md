# byke
How comfortable are bike lanes? And how can road surface quality be measured? This project explores the feasability of quantifying the bicycle lane surface roughness using an accelerometer. To guarantee a broad application, this project uses mobile devices for data collection


## How to use the data processor 
To acquire data, a mobile device is needs to be placed in a fixed position on a bicycle frame (best handlebar). As of now, the input data is generated with the free Android/iOs application "Physics Toolbox" (version 1.9.3.7). With the 'multireport' feature in the app we need to record 'g-force' and 'position'. 
To run the processor on a dataset, use ```python -W ignore process.py /<input>.csv <outputname> ```.

## Resulting data
What we're left with after processing is the "Happy-Bike-Index" (HBI) exported as geoJSON Line-Features. The ```data/processed/citytracks``` folder contains several sample datasets. The processed data is stored with the parameter specifications in the filename, that were applied on the datasets:
- c: cutoff frequency (best 1 Hz)
- s: timeframe size (best 2s)
- t: thresholding value (best 1.5 times g-force) 

Due to hardware caused GPS errors of the tracking device, the datasets of tracks 1-6 have flawed Features. These issues (if not to grave) can to be manipulated in a GIS. Track 7 and 8 show promising results. 

## What the processor does

![alt text](https://github.com/schienenersatzverkehr/byke/blob/master/HBI2.png) 
The data is processed in the following steps: 
1. Input is generated with Physics tool box with an unknown sample distance of T
2. The input is assumed as a Time discrete signal 
3. A dynamic threshold is applied with timeframe size (s) and threshold (z_t)
4. Highpass Butterworth filter with cutofffrequency (omega) generates a highpassed signal
5. The floating root mean square with timeframe size (s) caculates average over time 
6. To get a spatial represantiation, another average is calculated but only over a unique Geotag
7. To get an Index, the averages are normalized between 0 (good) and 1 (bad)
