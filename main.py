import csv
import datetime
import json
import time
import urllib.request
import zipfile

import wget

start = time.time()

url_cases = "https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.json"
url_vacc = "https://epistat.sciensano.be/Data/COVID19BE_VACC.json"
url_population = "https://statbel.fgov.be/sites/default/files/files/opendata/bevolking%20naar%20woonplaats%2C%20nationaliteit%20burgelijke%20staat%20%2C%20leeftijd%20en%20geslacht/TF_SOC_POP_STRUCT_2021.zip"

contents = urllib.request.Request(url_population,
                                  headers={'Content-Type': 'application/zip', 'User-Agent': 'Mozilla/5.0'})

wget.download(url_vacc, './downloads/COVID19BE_VACC.json')
wget.download(url_population, './downloads/TF_SOC_POP_STRUCT_2021.zip')

data_json_cases = 0
data_json_vacc = 0

with zipfile.ZipFile('./downloads/TF_SOC_POP_STRUCT_2021.zip', 'r') as zip_ref:
    zip_ref.extractall('./downloads/')

with open("./downloads/COVID19BE_CASES_AGESEX.json") as file:
    data_json_cases = json.loads(file.read())

with open("./downloads/COVID19BE_VACC.json") as file:
    data_json_vacc = json.loads(file.read())

hash_population_age = {
    "Flanders": {'0-17': 0, '18-34': 0, '35-44': 0, '45-54': 0, '55-64': 0, '65-74': 0, '75-84': 0, '85+': 0},
    "Wallonia": {'0-17': 0, '18-34': 0, '35-44': 0, '45-54': 0, '55-64': 0, '65-74': 0, '75-84': 0, '85+': 0},
    "Brussels": {'0-17': 0, '18-34': 0, '35-44': 0, '45-54': 0, '55-64': 0, '65-74': 0, '75-84': 0, '85+': 0},
    "Ostbelgien": {'0-17': 0, '18-34': 0, '35-44': 0, '45-54': 0, '55-64': 0, '65-74': 0, '75-84': 0, '85+': 0}
}

with open("./downloads/TF_SOC_POP_STRUCT_2021.txt", newline='') as file:
    values = csv.reader(file, delimiter='|', )
    for row in values:
        if row[1] == "TX_DESCR_NL":
            continue  # Skip the header of the file
        if row[10] == 'Vlaams Gewest':
            if int(row[19]) <= 17:
                hash_population_age["Flanders"]['0-17'] += int(row[20])
            elif int(row[19]) <= 34:
                hash_population_age["Flanders"]['18-34'] += int(row[20])
            elif int(row[19]) <= 44:
                hash_population_age["Flanders"]['35-44'] += int(row[20])
            elif int(row[19]) <= 54:
                hash_population_age["Flanders"]['45-54'] += int(row[20])
            elif int(row[19]) <= 64:
                hash_population_age["Flanders"]['55-64'] += int(row[20])
            elif int(row[19]) <= 74:
                hash_population_age["Flanders"]['65-74'] += int(row[20])
            elif int(row[19]) <= 84:
                hash_population_age["Flanders"]['75-84'] += int(row[20])
            else:
                hash_population_age["Flanders"]['85+'] += 1
        elif row[10] == 'Waals Gewest':
            if int(row[19]) <= 17:
                hash_population_age["Wallonia"]['0-17'] += int(row[20])
            elif int(row[19]) <= 34:
                hash_population_age["Wallonia"]['18-34'] += int(row[20])
            elif int(row[19]) <= 44:
                hash_population_age["Wallonia"]['35-44'] += int(row[20])
            elif int(row[19]) <= 54:
                hash_population_age["Wallonia"]['45-54'] += int(row[20])
            elif int(row[19]) <= 64:
                hash_population_age["Wallonia"]['55-64'] += int(row[20])
            elif int(row[19]) <= 74:
                hash_population_age["Wallonia"]['65-74'] += int(row[20])
            elif int(row[19]) <= 84:
                hash_population_age["Wallonia"]['75-84'] += int(row[20])
            else:
                hash_population_age["Wallonia"]['85+'] += 1
        elif row[10] == 'Brussels Hoofdstedelijk Gewest':
            if int(row[19]) <= 17:
                hash_population_age["Brussels"]['0-17'] += int(row[20])
            elif int(row[19]) <= 34:
                hash_population_age["Brussels"]['18-34'] += int(row[20])
            elif int(row[19]) <= 44:
                hash_population_age["Brussels"]['35-44'] += int(row[20])
            elif int(row[19]) <= 54:
                hash_population_age["Brussels"]['45-54'] += int(row[20])
            elif int(row[19]) <= 64:
                hash_population_age["Brussels"]['55-64'] += int(row[20])
            elif int(row[19]) <= 74:
                hash_population_age["Brussels"]['65-74'] += int(row[20])
            elif int(row[19]) <= 84:
                hash_population_age["Brussels"]['75-84'] += int(row[20])
            else:
                hash_population_age["Brussels"]['85+'] += int(row[20])
        else:
            if int(row[19]) <= 17:
                hash_population_age["Ostbelgien"]['0-17'] += int(row[20])
            elif int(row[19]) <= 34:
                hash_population_age["Ostbelgien"]['18-34'] += int(row[20])
            elif int(row[19]) <= 44:
                hash_population_age["Ostbelgien"]['35-44'] += int(row[20])
            elif int(row[19]) <= 54:
                hash_population_age["Ostbelgien"]['45-54'] += int(row[20])
            elif int(row[19]) <= 64:
                hash_population_age["Ostbelgien"]['55-64'] += int(row[20])
            elif int(row[19]) <= 74:
                hash_population_age["Ostbelgien"]['65-74'] += int(row[20])
            elif int(row[19]) <= 84:
                hash_population_age["Ostbelgien"]['75-84'] += int(row[20])
            else:
                hash_population_age["Ostbelgien"]['85+'] += int(row[20])

hash_gewesten = dict()
hash_gewesten_vacc = dict()
hash_gewesten_vacc_age = {"Flanders": dict(), "Wallonia": dict(), "Brussels": dict(), "Ostbelgien": dict()}
hash_population = {"Flanders": 6653062, "Wallonia": 3648206, "Brussels": 1219970}

for element in data_json_cases:
    if 'REGION' not in element:
        if 'Undefined' in hash_gewesten:
            hash_gewesten['Undefined'] += element['CASES']
        else:
            hash_gewesten['Undefined'] = element['CASES']
        continue
    if element['REGION'] in hash_gewesten:
        hash_gewesten[element['REGION']] += element['CASES']
    else:
        hash_gewesten[element['REGION']] = element['CASES']

for element in data_json_vacc:
    if 'REGION' not in element:
        if 'Undefined' in hash_gewesten_vacc:
            hash_gewesten_vacc['Undefined'] += element['COUNT']
        else:
            hash_gewesten_vacc['Undefined'] = element['COUNT']
        continue
    if element['REGION'] in hash_gewesten_vacc:
        if element['AGEGROUP'] in hash_gewesten_vacc_age[element['REGION']]:
            if element['DOSE'] in ["B", "C"] and ((datetime.datetime.strptime(element['DATE'], '%Y-%m-%d') +
                                                   datetime.timedelta(weeks=2)) <= datetime.datetime.now()):
                hash_gewesten_vacc_age[element['REGION']][element['AGEGROUP']] += element['COUNT']
        else:
            if element['DOSE'] in ["B", "C"] and ((datetime.datetime.strptime(element['DATE'], '%Y-%m-%d') +
                                                   datetime.timedelta(weeks=2)) <= datetime.datetime.now()):
                hash_gewesten_vacc_age[element['REGION']][element['AGEGROUP']] = element['COUNT']
        if element['DOSE'] in ["B", "C"] and ((datetime.datetime.strptime(element['DATE'], '%Y-%m-%d') +
                                               datetime.timedelta(weeks=2)) <= datetime.datetime.now()):
            hash_gewesten_vacc[element['REGION']] += element['COUNT']
    else:
        if element['DOSE'] in ["B", "C"] and ((datetime.datetime.strptime(element['DATE'], '%Y-%m-%d') +
                                               datetime.timedelta(weeks=2)) <= datetime.datetime.now()):
            hash_gewesten_vacc[element['REGION']] = element['COUNT']

for key in hash_gewesten:
    if key == 'Undefined':
        print(f'Cases of an Undefined region:\t\t\t {hash_gewesten[key]}')
        print(f'Vaccinations in an Undefined region:\t {hash_gewesten_vacc[key]}')
    else:
        print(f'Cases per 100k people for {key}:\t\t\t {hash_gewesten[key] / (hash_population[key] / 100)}%')
        print(f'Vaccinations per 100k people for {key}:\t {hash_gewesten_vacc[key] / (hash_population[key] / 100)}%')

print(hash_population_age)

for key in hash_gewesten_vacc_age:
    print(f'{key}')
    for key2 in hash_gewesten_vacc_age[key]:
        if hash_population_age[key][key2] != 0:
            print(f'{key2} :: {hash_gewesten_vacc_age[key][key2] / (hash_population_age[key][key2] / 100)}%')

end = time.time()

print("total time = ", end - start)
