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

# table_texts = []
# for tt in soup.find_all("table"):
#     # table_texts.append(tt)
#     print(tt.text)

# exit(0)

# Extract data from the webpage
people = soup.table.text

# Clean the extracted data
people = people.split(" ")
while '' in people:
    people.remove('')
people_list = []
for i, p in enumerate(people):
    if p[0] in CAPITALS:
        people_list.append(p)
    elif p[0] in LOWERCAS:
        people_list[-1] = people_list[-1] + " " + p
    elif p[0] in PUNCTUAS:
        people_list[-1] = people_list[-1] + " " + p
    elif p[0] in NUMBERS:
        pi = p.replace(',', '')
        people_list.append(pi)
    else:
        people_list.append(p)

# Create a DataFrame
# data = {'Column1': [value1], 'Column2': [value2]}
data = {}
col_name = ""
for j, pl in enumerate(people_list):
    if pl[0] not in NUMBERS:
        col_name = pl
        data[pl] = [0]
    else:
        data[col_name] = [int(pl)]

df = pd.DataFrame(data)

# Export the DataFrame to an Excel file
df.T.to_excel('output.xlsx')
