import netCDF4
import numpy as np
import os


curr_dir_files = os.listdir('C:/Users/KeneilweH/Desktop/CCSM4_RCP45/Climate_models_1983_2005/2005/')
#wdir='C:/Users/KeneilweH/Desktop/ACCESS_RCP85'


input_files = []
for f in curr_dir_files:
    if f.endswith('.nc'):
        input_files.append(f)

datasets = []
for input_file in input_files:
    if input_file == 'T_output_file':
        continue
    inputDS = netCDF4.Dataset('C:/Users/KeneilweH/Desktop/CCSM4_RCP45/Climate_models_1983_2005/2005/' + input_file,'r', format='NETCDF4')
    print(inputDS['tmaxscr'])
    datasets.append(inputDS)

lat_dim_len = len(datasets[0]['lat'])
lon_dim_len = len(datasets[0]['lon'])
time_dim_len = len(datasets[0]['time'])
#1
#creating an empty np array of zeros
tmaxscr_mean = np.zeros([lat_dim_len, lon_dim_len])

#rnd24_aggregate = datasets[0]['rnd24'][0][:][:]
 
#calculate the mean/sum
for i, dataset in enumerate(datasets, 1):
    #append to rnd24_aggregate
    tmean = np.nanmean(dataset['tmaxscr'], axis=0)
    #calculate the mean/sum
    #rnd24_aggregate =np.nansum(rnd24_aggregate,axis=0)
    #tmaxscr_mean = tmaxscr_mean/len('time')
    #rnd24_aggregate = rnd24_aggregate/len(dataset)
    print(tmean)

#print(rnd24_aggregate[0][99][0])
#print(datasets[0]['rnd24'][0][75][75])

    #### Create output netcdf ####
    
    T_output_file = '2005Temp_monthly_output%d.nc' % i 

    outDS = netCDF4.Dataset(T_output_file,'w', format='NETCDF4')
    
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
    tmaxscr_mean[:,:] = tmean[:][:]
    
    outDS.close()
