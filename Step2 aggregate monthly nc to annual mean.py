# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:25:04 2019

@author: KeneilweH
"""

import netCDF4
import numpy as np
import os

curr_dir_files = os.listdir('C:/Users/KeneilweH/Desktop/ACCESS_RCP85/Climate_models_2046_2065/monthly Temp mean/2065')

input_files = []
for f in curr_dir_files:
    if f.endswith('.nc'):
        input_files.append(f)

datasets = []
for input_file in input_files:
    if input_file == 'output.nc':
        continue
    inputDS = netCDF4.Dataset('C:/Users/KeneilweH/Desktop/ACCESS_RCP85/Climate_models_2046_2065/monthly Temp mean/2065/' + input_file,'r', format='NETCDF4')
    print(inputDS['tmaxscr_mean'])
    datasets.append(inputDS)

lat_dim_len = len(datasets[0]['lat'])
lon_dim_len = len(datasets[0]['lon'])
#time_dim_len = len(datasets[0]['time'])

#creating an empty np array of zeros
t_sum = np.zeros([lat_dim_len, lon_dim_len])


#calculate the mean/sum
for i, dataset in enumerate(datasets, 1):
    #append to rnd24_aggregate
    #t_mean_annual = np.nanmean(dataset['tmaxscr_mean'], axis=0)
    #t_mean_annual = tmaxscr_mean_annual[:][:][:] + dataset['tmaxscr_mean'][0][:][:]
    t_sum += dataset['tmaxscr_mean']
    #t_mean_annual =  tmaxscr_mean_annual/len(datasets)
    #rnd24_aggregate = rnd24_aggregate/len(dataset)
  
t_mean_annual = t_sum / 12
print(t_mean_annual)


    #### Create output netcdf ####
output_file = '2065_annual_temp.nc' 

outDS = netCDF4.Dataset(output_file,'w', format='NETCDF4')
    
lat_dim = outDS.createDimension('lat',lat_dim_len)
lon_dim = outDS.createDimension('lon',lon_dim_len)
    #time_dim = outDS.createDimension('time', time_dim_len)
    
latitude = outDS.createVariable('lat',np.float32,('lat',))
latitude.units = 'degrees_north'
latitude.standard_name = 'latitude'
                
longitude = outDS.createVariable('lon',np.float32,('lon',))
longitude.units = 'degrees_east'
longitude.standard_name = 'longitude'
                
#    time = outDS.createVariable('time',np.int32,('time',))
#    time.standard_name = 'time'
#    time.units = 'seconds since 1983-01-01 00:00:00'
#    time.calendar = 'gregorian'
    
latitude[:] = datasets[0]['lat'][:]
longitude[:] = datasets[0]['lon'][:]
    #time[:] = datasets[0]['time'][0]
    
tmaxscr_mean = outDS.createVariable('tmaxscr_mean',np.float32,('lat','lon'),zlib=True)
tmaxscr_mean[:,:] = t_mean_annual[:][:]
    
outDS.close()
