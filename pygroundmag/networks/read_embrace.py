#%%
from pygroundmag.utils.library_functions import *
import pytplot
import pandas as pd
from loguru import logger as logging
#%%
def readEmbrace(files, station_list, usePandas, usePyTplot):
    ######
    ## Abre os arquivos e extrai as componentes
    #
    global fulldate_array
    variables_dataframe = dict()
    tplot_vars = list()
    for station in station_list:
        out_dataFrame = list()
        for f in files:
            logging.info(f)
            resolution_data = f.split('.')[-1][-1]

            try:
                temp_data = np.loadtxt(f, skiprows=4, usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9), unpack=True)

                b_H = temp_data[6, :]
                b_D = temp_data[5, :]
                b_Z = temp_data[7, :]
                b_I = temp_data[8, :]
                b_F = temp_data[9, :]
                dia = temp_data[0, :]
                mes = temp_data[1, :]
                ano = temp_data[2, :]
                hora = temp_data[3, :]
                min = temp_data[4, :]
                mean_H = b_H - np.nanmean(b_H)

                t = [datetime.datetime(int(ano[i]), int(mes[i]), int(dia[i]), int(hora[i]), int(min[i])) for i in
                     range(0, len(dia))]


                if resolution_data == 'm':
                    fulldate_array = pd.date_range(start=f'{int(ano[0])}-{int(mes[0])}-{int(dia[0])}', periods=24*60, freq='min')
                if resolution_data == 's':
                    fulldate_array = pd.date_range(start=f'{int(ano[0])}-{int(mes[0])}-{int(dia[0])}', periods=24*60*60, freq='s')

                data_array = np.transpose([b_H, b_D, b_Z, b_I, b_F, mean_H])
                columns = ['H', 'D', 'Z', 'I', 'F', 'mH']
                df_data = pd.DataFrame(data_array, index=t, columns=columns)
                df = df_data.reset_index().drop_duplicates(subset='index').set_index('index').sort_index()
                df_data_filled = df.reindex(fulldate_array, fill_value=np.nan).interpolate(method='linear')
                time_sec = [i.timestamp() for i in df_data_filled.index]

                df_data_filled.insert(0, 'ts', time_sec, True)

                out_dataFrame.append(df_data_filled)
            except (Exception) as e:
                logging.error(e)
                logging.info(f"File {f} corrupted")

        tplot_var = f"B_xyzh{station}"

        mag_dataFrame = pd.concat(out_dataFrame)

        mag_dataFrame.sort_index(inplace=True)
        if usePandas == True:
            variables_dataframe[tplot_var] = mag_dataFrame

        if usePyTplot == True:
            new_columns = mag_dataFrame.columns
            tplot_vars.append(tplot_var)
            ara_vars = np.asarray(mag_dataFrame[new_columns].values)
            attr_dict = {'columns': new_columns}
            dd_plot = pytplot.store_data(tplot_var, data={'x': mag_dataFrame['ts'].values, 'y': ara_vars},
                                         attr_dict=attr_dict)

    if usePyTplot == True:
        logging.warning("Using tplot variables!!")
        return tplot_vars
    if usePandas == True:
        logging.warning(("Using Pandas Data Frame!!"))
        return variables_dataframe