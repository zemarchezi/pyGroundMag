# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#%%
from pygroundmag.loaders.load import *
import json
import datetime
import aacgmv2


with open('/home/jose/python_projects/pyGroundMag/pygroundmag/utils/resources/config_file.json', 'r') as f:
    config_file = json.load(f)

#%%

# stations=['RANK', 'ESKI', 'FCHU', 'BACK', 'GILL', 'OXFO', 'ISLL', 'LGRR', 'PINA', 'THRF', 'OSAK']
stations=['ISLL']
# stations = ['CXP']

# %%
trange=['2021-04-05', '2021-04-06']
varss = load_mag(trange=trange, magnetometer='FGM',
             network='carisma',
             cadence='1Hz', station=stations,
             if_cdf=False, downloadonly=False,
             usePandas=True, config_file=config_file)


#%%
dt = datetime.datetime.strptime('20210112', '%Y%m%d')
mag = pyIGRF.igrf_value(lat=53.856, lon=265.34, alt=100., year=dt.year)
mag = {'decl': mag[0],
       'incl': mag[1],
       'horiz': mag[2],
       'north': mag[3],
       'east': mag[4],
       'down': mag[5],
       'total': mag[6]
}

#%%
cgm_lat, cgm_lon, cgm_r = aacgmv2.convert_latlon(53.856, 265.34, 100., dt, method_code='G2A')
