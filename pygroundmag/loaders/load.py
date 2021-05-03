from pygroundmag.utils.dailynames import dailynames
from pygroundmag.utils.download import download
from pygroundmag.utils.download_embrace import downloadEmbrace
from pygroundmag.networks.read_carisma import *
from pygroundmag.networks.read_embrace import *
from pathlib import Path
import glob

# %%
def load_mag(trange: list = ['2018-11-5', '2018-11-6'],
         magnetometer: str = 'FGM',
         cadence: str = '1Hz',
         station: list = ['FCHU'],
         if_cdf: bool = False,
         network: str = 'carisma',
         get_support_data: bool = False,
         varformat: str = None,
         varnames: list = [],
         downloadonly: bool = False,
         notplot: bool = False,
         no_update: bool = False,
         time_clip: bool = False,
         usePandas: bool = True,
         usePyTplot: bool = False,
         config_file: dict = {}):

    remote_path = config_file[network]['remote_data_dir']
    logging.info(f'Remotepath: {remote_path}')
    local_path = str(Path.home().joinpath(config_file[network]['local_data_dir'], network))
    logging.info(f'Local Download Path: {local_path}')



    out_files = []
    read_stations = []
    for stat in station:
        if network == 'carisma':
            if if_cdf:
                pathformat = f"{magnetometer}/CDF{cadence}/%Y/%m/%d/CARISMA_{magnetometer}_{cadence.lower()}_{stat.lower()}_%Y%m%d_v01.cdf"
            else:
                pathformat = f"{magnetometer}/{cadence}/%Y/%m/%d/%Y%m%d{stat}.F01.gz"
            # find the full remote path names using the trange
            remote_names = dailynames(file_format=pathformat, trange=trange)

            files = download(remote_file=remote_names, remote_path=remote_path,
                             local_path=local_path, no_download=no_update)
        if network == 'embrace':

            # exectSele = str(Path.home().joinpath(config_file[network]['executable_path']))
            #
            # print(exectSele)

            logging.warning(f'Station  ---  {stat}')

            files = downloadEmbrace(url=remote_path,
                     instrument=magnetometer, station=stat,
                     username=config_file[network]['usr'],
                     password=config_file[network]['pwd'],
                     trange=trange,
                     downloadDir=f'{local_path}/temp_download',
                     localDirPath=f'{local_path}/mag',
                     executable_path=config_file[network]['executable_path'])

            # dasr = trange[0].split('-')
            # pathformat = f"{remote_path}/{stat}/{dasr[0]}_{dasr[1]}_{dasr[2]}*/*.*m"
            # files = glob.glob(pathformat)

        if files is not None and len(files) > 0:
            read_stations.append(stat)
            for file in files:
                out_files.append(file)

    out_files = sorted(out_files)

    print(out_files)
    print(read_stations)

    if downloadonly:
        return out_files

    logging.info('Reading files')
    if len(out_files) > 0:
        if network == 'carisma':
            vars = readData(out_files, read_stations, usePyTplot=usePyTplot, usePandas=usePandas)
        if network == 'embrace':
            vars = readEmbrace(out_files, read_stations, usePyTplot=usePyTplot, usePandas=usePandas)

        return vars

    return []
