from typing import List
from loguru import logger as logging
import gzip
from pygroundmag.utils.library_functions import *

def readData(files, stations_list, usePyTplot, usePandas):
    ######
    ## Abre os arquivos e extrai as componentes
    #
    global latitude_geo, l_McIlwain, dict_coords
    variables_dataframe = dict()
    tplot_vars = list()
    for ss in stations_list:
        latitude: List[str]
        latitude, lshell = [], []
        cgm_latitude, cgm_longitude = [], []
        x, y, z, h, d, mh, t, stations, time_seconds = [], [], [], [], [], [], [], [], []
        stat_files = [f for f in files if ss in f]
        for i in stat_files:
            logging.info(f"Readding values from {i}")

            if i.split('.')[-1] == 'gz':
                logging.warning(f"the extension is .gz")
                f = gzip.open(i, 'rb')
                first_line = f.read().decode().split('\n')[0].split(' ')  ## Open the file and read the first line
                f.close()
            else:
                logging.warning(f"the extension is .txt")
                f = open(i, 'r')
                first_line = f.readline().split(' ')  ## Open the file and read the first line
                f.close()

            station = first_line[0]
            latitude_geo = first_line[2]
            longitude_geo = first_line[3]
            reference_date = first_line[4]
            temp_data = np.loadtxt(i, skiprows=1, usecols=(0, 1, 2, 3), unpack=True)
            temp_t = temp_data[0, :]
            temp_x = temp_data[1, :]
            temp_y = temp_data[2, :]
            temp_z = temp_data[3, :]

            logging.info(f"latitude_geo, {latitude_geo}")
            ######
            ## Open and read the x, y, and z compoents
            #
            logging.info(first_line)
            logging.warning(reference_date)
            logging.warning([latitude_geo, longitude_geo])
            dict_coords = convert_coords(date=reference_date,
                                         lat_long=[float(latitude_geo), float(longitude_geo)],
                                         altitude_km=100.)

            dec = float(dict_coords['declination'])

            temp_h = temp_x.astype(float) * np.cos(np.deg2rad(dec)) + \
                     temp_y.astype(float) * np.sin(np.deg2rad(dec))  # Calculate the H component
            temp_mh = temp_h - (np.mean(temp_h))  # Subtract the mean value of the field

            temp_d = temp_y.astype(float) * np.cos(np.deg2rad(dec)) - \
                     temp_x.astype(float) * np.sin(np.deg2rad(dec))
            #####
            ## Create an time array from the data
            time = [datetime.datetime.strptime(str(int(x)), "%Y%m%d%H%M%S") for x in temp_t]
            ## Second dta array
            # time_sec = [int(str(int(i))[8:10]) * 3600 + int(str(int(i))[10:12]) * 60 + int(str(int(i))[12:14]) for i in
            #             temp_t]
            time_sec = [i.timestamp() for i in time]

            station_list = [station] * len(time)  # Create an list with the stations names

            latitude_geo_list = [float(latitude_geo)] * len(time)  # Create a list with the corresponding latitudes
            cgm_latitude_list = [float(dict_coords['cgm_latitude'])] * len(time)
            cgm_longitude_list = [float(dict_coords['cgm_longitude'])] * len(time)
            l_McIlwain = [float(dict_coords['lshell'])] * len(time)  # McIlwain parameter

            ## Create an list with the components for each station
            t.extend(time)  # time array
            x.extend(temp_x.astype(float))  # x component
            y.extend(temp_y.astype(float))  # y component
            z.extend(temp_z.astype(float))  # z component
            h.extend(temp_h.astype(float))  # H component
            mh.extend(temp_mh.astype(float))  # mean variation of H component
            d.extend(temp_d.astype(float))
            time_seconds.extend(time_sec)
            stations.extend(station_list)
            latitude.extend(latitude_geo_list)
            cgm_latitude.extend(cgm_latitude_list)
            cgm_longitude.extend(cgm_longitude_list)
            lshell.extend(l_McIlwain)

        tplot_var = f"B_xyzh{ss}"
        tplot_vars.append(tplot_var)
        ara_vars = np.asarray(np.transpose([x, y, z, h, mh, d]))
        attr_dict = dict(columns=['x', 'y', 'z', 'h', 'mean_h', 'd'], station=ss, latitude=latitude_geo,
                         l_shell=l_McIlwain[0], cgm_latitude=dict_coords['cgm_latitude'],
                         cgm_longitude=dict_coords['cgm_longitude'])

        if usePyTplot == True:
            import pytplot
            dd_plot = pytplot.store_data(tplot_var, data={'x': time_seconds, 'y': ara_vars}, attr_dict=attr_dict)

        if usePandas == True:
            import pandas as pd
            print('Using Pandas!')
            daast = [x, y, z,
                     h, mh, d, stations,
                     latitude, lshell, cgm_latitude,
                     cgm_longitude, time_seconds]
            dd = pd.DataFrame(np.transpose(daast),
                              index=t, columns=['x', 'y', 'z', 'h', 'mean_h', 'd', 'stat', 'lat', 'lshell', 'gcm_lat', 'gcm_lon', 'time_seconds'])
            variables_dataframe[tplot_var] = dd



    if usePyTplot == True:
        logging.warning("Using tplot variables!!")
        return tplot_vars
    if usePandas == True:
        logging.warning(("Using Pandas Data Frame!!"))
        return variables_dataframe