from io import BytesIO
import requests, os, zipfile, logging
from datetime import date
from requests.models import Response
import pandas as pd

# lists are easy to be replaced by txt files
names = [
         'ROBERTO FURIAN ARDENGHY',
         'NICOLAS SIMONE',
         'JOAQUIM SILV E LUNA',
         'CLAUDIO ROGERIO LINASSI MASTELLA',
         'RODRIGO ARAUJO ALVES',
         'FERNANDO ASSUMPCAO BORGES',
         'JOAO HENRIQUE RITTERSHAUSSEN',
         'RODRIGO COSTA LIMA E SILVA',
         'SALVADOR DAHAN',
         ]

# dictionary just to separate the strings
# the ideal is to create a file called "constants"
result = {
    True: "É PPE",
    False: "NÃO É PPE",
}

url = 'http://www.portaldatransparencia.gov.br/download-de-dados/pep/'

# this function takes the url and makes a GET request
# in order to download the file, saving it in the project folder

def download_pep(url: str, address: str = None) -> None:

    # getting relative address
    if not address:
        address = os.path.basename(url.split("?")[0])

    # GET request with HTTP protocol
    response = requests.get(url)

    # validating the URL
    if response.status_code == requests.codes.OK:
        # opening folder in binary write mode
        with open(address, 'wb') as new_file:
            # saving request in directory
            new_file.write(response.content)
        logging.info(f'successful download of {url}')
        logging.info(f'saved in {address}')
        # function created to unzip, more information below
        extract_zip(response)
    else:
        response.raise_for_status()



# in cases where it is interesting to change the date
# the function below formats the url validating the
# types that are entering and concatenating the parameters
def format_url(url: str, date: date) -> str:
    date_req = date.strftime("%Y%m")
    return url+date_req


def extract_zip(req: Response) -> None:
    z = zipfile.ZipFile(BytesIO(req.content))
    z.extractall(os.getcwd())


url_request = format_url(url=url, date=date(2021, 11, 1))


download_pep(url_request)

data = pd.read_csv('./202111_PEP.csv', sep=';', encoding="ISO-8859-1")
select_column = data['Nome_PEP']

# filling dictionary with "NÃO É PPE"
output = {name: result.get(False) for name in names}

# scan the dataframe in the name column, if it finds any of
# the names in the list, the value in the output dictionary is changed
for name in names:
    if len(select_column[select_column == name].values) != 0:
        output[name] = result.get(True)

# printing the result on the screen
for v, k in output.items():
    print(f'{v} - {k}')
