from loguru import logger as logging
import pytz
from pygroundmag.utils.library_functions import *

def readSupermag(stations_dict, usePyTplot, usePandas):
    ######
    ## Abre os arquivos e extrai as componentes
    #
    global latitude_geo, l_McIlwain, dict_coords

    for ss in stations_dict.keys():

        if usePyTplot == True:
            import pytplot
            # dd_plot = pytplot.store_data(tplot_var, data={'x': time_seconds, 'y': ara_vars}, attr_dict=attr_dict)
            pass

        if usePandas == True:
            import pandas as pd
            print('Using Pandas!')

            data = stations_dict[ss]
            tims = [datetime.datetime.fromtimestamp(i, pytz.timezone("UTC")) for i in data.tval]
            data.index = tims
            stations_dict[ss] = data



    if usePyTplot == True:
        logging.warning("Using tplot variables not available at the moment!!")
        return stations_dict
    if usePandas == True:
        logging.warning(("Using Pandas Data Frame!!"))
        return stations_dict