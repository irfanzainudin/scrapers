import requests
from bs4 import BeautifulSoup
import pandas as pd

CAPITALS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWERCAS = "abcdefghijklmnopqrstuvwxyz"
PUNCTUAS = "("
NUMBERS = "0123456789"

# Send a GET request to the webpage
url = 'https://abs.gov.au/census/find-census-data/quickstats/2001/SSC12276'
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract data from the webpage
for idx, tt in enumerate(soup.find_all("table")):
    dt = tt.text

    # Clean the extracted data
    dt = dt.split(" ")
    while '' in dt:
        dt.remove('')
    dt_list = []
    for i, p in enumerate(dt):
        if p[0] in CAPITALS:
            dt_list.append(p)
        elif p[0] in LOWERCAS:
            dt_list[-1] = dt_list[-1] + " " + p
        elif p[0] in PUNCTUAS:
            dt_list[-1] = dt_list[-1] + " " + p
        elif p[0] in NUMBERS:
            pi = p.replace(',', '')
            dt_list.append(pi)
        else:
            dt_list.append(p)

    # Create a DataFrame
    # data = {'Column1': [value1], 'Column2': [value2]}
    data = {}
    col_name = ""
    for j, pl in enumerate(dt_list):
        if pl[0] not in NUMBERS:
            col_name = pl
            data[pl] = [0]
        else:
            if '.' not in pl:
                data[col_name] = [int(pl)]
            else:
                data[col_name] = [float(pl)]

    df = pd.DataFrame(data)

    # Export the DataFrame to an Excel file
    df.T.to_excel(f"output{idx}.xlsx")
