# Basic documentation for pyGroundMag


## Requirements


Python 3.8+

Pandas, NumPy, wget, requests, cdflib, pytplot

***
### Chrome Driver

Please check your version of Google Chrome Web Browser. The Chromedriver must be the same version

The Chromedriver can be downloaded at: https://chromedriver.chromium.org/downloads

download and unzip the file to:
```pygroundmag/utils/resources/chromedriver_linux64/```

***

Installation: ```pip instal -e .```

***
## config_file.json

If some change in downloding directories is needed, it can be done in this file.

```pygroundmag/utils/resources/config_file.json```

This file sets the http directory for downloading data and the local directory to download data.

The local directory files are organized as http directory, i.e.:
* Embrace: HOME/mag_data/embrace/Magnetometer/CXP/YYYY/filename.YYm

This files handles with the different http subpaths for the different levels and intruments in each probe.

***

```python
import json
from pygroundmag.loaders.load import *

trange=['2021-05-26', '2021-05-30']

varss_mag = load_mag(trange=trange, magnetometer='magnetometer',
                     network='embrace',
                     cadence='1Hz', station=['VSS', 'SMS', 'CHI', 'MED', 'JAT', 'CXP'],
                     if_cdf=False, downloadonly=False,
                     usePandas=True, usePyTplot=False, config_file=config_file_mag)
