
import selenium
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
import time
from zipfile import ZipFile
import os
from loguru import logger as logging
import glob
#%%


def extractFiles(file_list: list=[], localDirPath:str=''):

    outFilesList = []



    for i in file_list:
        logging.info(f'Opening {i}')
        with ZipFile(i, 'r') as zipObj:
            logging.info(zipObj.printdir())

            files = zipObj.namelist()

            for j in files:
                outFilesList.append(f'{localDirPath}/{j}')

            logging.info('Extracting all the files')

            zipObj.extractall(path=localDirPath)

            logging.info('Done Unzip')

    return outFilesList



def downloadEmbrace(url: str='',
                     instrument: str='Magnetometer',
                     station: str='SJC',
                     username: str='',
                     password: str='',
                     trange: list=[],
                     downloadDir: str='',
                     localDirPath: str='',
                     executable_path: str=''):

    stationsDict = {'ARA': 'Araguatins',
               'CHI': 'Chillán',
               'CXP': 'Cachoeira Paulista',
               'MAN': 'Manaus',
               'CBA': 'Cuiabá',
               'SJC': 'São José dos Campos',
               'SLZ': 'São Luís',
               'MED': 'Medianeira',
               'TCM': 'Tucuman',
               'JAT': 'Jataí',
               'PVE': 'Porto Velho',
               'VSS': 'Vassouras',
               'RGA': 'Rio Grande - Argentina',
               'ALF': 'Alta Floresta',
               'EUS': 'Eusébio',
               'SMS': 'São Martinho da Serra'}


    url1 = f'{url}/accounts/login/'
    url2 = f'{url}/search/'

    if not os.path.exists(downloadDir):
        os.makedirs(os.path.dirname(downloadDir))

    filename = f"{downloadDir}/{stationsDict[station]}_swdatashare-{trange[0]}-to-{trange[1]}.zip"
    if os.path.isfile(filename) == True:
        logging.info('File is current: ' + filename)

        outFiles = extractFiles(file_list=[filename], localDirPath=localDirPath)

        return outFiles

    station = stationsDict[station]

    files_before = glob.glob(f"{downloadDir}/*.zip")
    chromeOptions = Options()
    # chromeOptions.headless = True
    chromeOptions.add_experimental_option("prefs", {"download.default_directory": f"{downloadDir}",
                                                    "download.prompt_for_download": False,
                                                    "download.directory_upgrade": True, "safebrowsing.enabled": True})

    driver = selenium.webdriver.Chrome(options=chromeOptions, executable_path=executable_path) # Alternately, give Chrome a try
    print('\tDone')


    logging.info('Retrieving initial web page')
    driver.get(url1)
    logging.info('\tDone')
    time.sleep(2)
    user = driver.find_element_by_id("id_username")
    time.sleep(2)
    logging.info('set Username')
    user.send_keys(f'{username}')
    time.sleep(2)
    passwd = driver.find_element_by_id("id_password")
    time.sleep(2)
    logging.info('Set Password')
    passwd.send_keys(f'{password}')
    time.sleep(2)
    logging.info('Login')
    driver.find_element_by_name("btn_login").click()
    time.sleep(2)
    logging.info('Changing to second URL')
    driver.get(url2)
    time.sleep(2)


    instrument_drop = driver.find_element_by_xpath('/html/body/ll/div[3]/div/div[3]/form/div/div[1]/div[1]/div/input').click()
    ulListInstr = driver.find_elements_by_tag_name('ul')
    time.sleep(2)
    logging.info('Getting instruments List')
    for item in ulListInstr:
        text = item.text

        if 'Magnetometer' in text:
            print (item.id)
            instrListId = item

    instr_items = instrListId.find_elements_by_tag_name("li")
    time.sleep(2)
    logging.info(f'Selecting Instrument to {instrument}')
    for item in instr_items:
        text = item.text
        if text == f'{instrument}':
            print (text)
            item.click()

    logging.info('Selecting date range')
    initialDate_drop = driver.find_element_by_xpath('//*[@id="dt1"]')
    initialDate_drop.send_keys(f'{trange[0]}')
    endDate_drop = driver.find_element_by_xpath('//*[@id="dt2"]')
    endDate_drop.send_keys(f'{trange[1]}')
    time.sleep(2)

    resol_drop = driver.find_element_by_xpath('/html/body/ll/div[3]/div/div[3]/form/div/div[2]/div[1]/div/input').click()
    ulListInstr = driver.find_elements_by_tag_name('ul')
    time.sleep(2)
    logging.info('Getting Resolution List options')
    for item in ulListInstr:
        text = item.text
        if 'Low (min)' in text:
            print (item.id)
            item.click()


    station_drop = driver.find_element_by_xpath('/html/body/ll/div[3]/div/div[3]/form/div/div[2]/div[2]/div/input').click()
    ulListInstr = driver.find_elements_by_tag_name('ul')
    time.sleep(2)
    logging.info('Getting stations List Options')
    for item in ulListInstr:
        text = item.text
        if 'Cachoeira Paulista' in text and 'Rio Grande' in text:
            print (item.id)
            stationsId = item

    itemsStations = stationsId.find_elements_by_tag_name("li")
    time.sleep(2)
    print(f'Selecting {station} Station')
    for item in itemsStations:
        text = item.text
        if text == station:
            print (text)
            item.click()


    driver.find_element_by_xpath('//*[@id="search-button"]').click()
    time.sleep(2)

    table = driver.find_element_by_xpath('/html/body/ll/div[3]/div/div[4]/form/table/tbody')

    itens_tables = table.find_elements_by_tag_name('tr')
    time.sleep(2)



    for tt in itens_tables:
        if len(itens_tables) > 0:
            tex = tt.text
            if tex == 'Sorry, there are no files for these filters..':
                logging.warning('No data')
                break
            else:
                logging.warning('There are data')
                download = True
                break


    if download == True:
        logging.info('Downloading Files')
        down = driver.find_element_by_id('downloads').click()

    logging.info('Download Finished')



    time.sleep(3)
    logging.info('Download Finished')
    files_after = glob.glob(f"{downloadDir}/*.zip")
    new_files = list(set(files_after).difference(files_before))

    logging.info(f'Compressed File downloaded to: {new_files}')
    driver.quit()

    logging.info(f'Rename Files')
    openFilesList = []
    for ff in new_files:
        filNAme = ff.split('/')[-1]
        filNewName = f'{station}_{filNAme}'
        newDirName = ff.replace(filNAme, filNewName)
        os.rename(ff, newDirName)
        openFilesList.append(newDirName)

    outFiles = extractFiles(file_list=openFilesList, localDirPath=localDirPath)

    return outFiles