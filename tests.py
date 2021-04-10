# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#%%
from pygroundmag.loaders.load import *
import json

# from src.read_embrace import *

with open('/home/jose/python_projects/pyGroundMag/pygroundmag/utils/resources/config_file.json', 'r') as f:
    config_file = json.load(f)

#%%

# stations=['RANK', 'ESKI', 'FCHU', 'BACK', 'GILL', 'OXFO', 'ISLL', 'LGRR', 'PINA', 'THRF', 'OSAK']
stations = ['CXP']

# %%
trange=['2021-03-22', '2021-03-24']
varss = load(trange=trange, magnetometer='FGM',
             network='embrace',
             cadence='1Hz', station=stations,
             if_cdf=False, downloadonly=False,
             usePandas=True, config_file=config_file)