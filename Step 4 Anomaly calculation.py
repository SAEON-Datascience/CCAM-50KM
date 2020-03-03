# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 09:49:09 2019

@author: KeneilweH
"""

import netCDF4
import numpy as np
import numpy.ma as ma

#Calculating anomaly, equation: Anomaly = Future data - baseline data
# Future dataset 

###############

f= netCDF4.Dataset ('C:/Users/KeneilweH/Desktop/CCSM4_RCP45/Anomalies/2046_2065_CCSM4_RCP45_temp.nc' ,'r', format='NETCDF4')
print(f)
print(f.variables.keys())
temp_2080_2099 = f.variables['tmaxscr_mean']  # temperature variable
print(temp_2080_2099)
f_tmean = ma.masked_invalid(f.variables['tmaxscr_mean'])#Mask array
input_files = f

datasets = []
datasets.append(input_files)
    
lat_dim_len = len(datasets[0]['lat'])
lon_dim_len = len(datasets[0]['lon'])

#creating an empty np array of zeros
t_anomaly = np.zeros([lat_dim_len, lon_dim_len])

#Baseline dataset
b = netCDF4.Dataset('C:/Users/KeneilweH/Desktop/CCSM4_RCP45/Anomalies/1983_2005_CCSM4_RCP45_temp.nc' ,'r', format='NETCDF4')
print(b)
print(b.variables.keys())
temp_1983_2005 =b.variables['tmaxscr_mean'] # temperature variable
print(temp_1983_2005) 

b_tmean = ma.masked_invalid(b.variables['tmaxscr_mean'])#Mask array

#Calculate Anomaly
Anomaly = f_tmean -b_tmean
print(Anomaly)

  #### Create output netcdf ####
output_file = 'Avg_2046_2065_CCSM4_RCP45.nc' 

outDS = netCDF4.Dataset(output_file,'w', format='NETCDF4')
    
lat_dim = outDS.createDimension('lat',lat_dim_len)
lon_dim = outDS.createDimension('lon',lon_dim_len)
    
latitude = outDS.createVariable('lat',np.float32,('lat',))
latitude.units = 'degrees_north'
latitude.standard_name = 'latitude'
                
longitude = outDS.createVariable('lon',np.float32,('lon',))
longitude.units = 'degrees_east'
longitude.standard_name = 'longitude'
                 
latitude[:] = datasets[0]['lat'][:]
longitude[:] = datasets[0]['lon'][:]

Anomaly_= outDS.createVariable('Anomaly',np.float32,('lat','lon'),zlib=True)
Anomaly_[:,:] = Anomaly[:][:]
      
outDS.close()


    






