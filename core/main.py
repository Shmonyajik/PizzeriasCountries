
from itertools import count
import urllib.request
import json
import sys
sys.path.insert(0, "C:\python\scrap_tutorial\googlesheetspars")
import quickstart



def JSONPars (url):
    with urllib.request.urlopen(url) as URL:
        data = json.load(URL)
    table = {}
    for country in data["countries"]:
        country_name = country["countryName"]
        for pizzeria in country["pizzerias"]:
           table[pizzeria["alias"]] = pizzeria["address"]["locality"]["name"]
            
            
        
    output = {
        country_name: table
    }
    
    return output

def main(): 
    combine = {**JSONPars("https://globalapi.dodopizza.com/api/v1/pizzerias/all/112"), **JSONPars("https://globalapi.dodopizza.com/api/v1/pizzerias/all/566")}
   
    pizza_values = [] 
    country_value =[]
    country_value1 =[]
    for value, key in combine["Беларусь"].items(): 
        country_value.append(['Беларусь'])
        pizza_values.append([value,key]) 
    for value, key in combine["Нигерия"].items():
        country_value1.append(['Нигерия'])
        pizza_values.append([value,key]) 
    gs = quickstart.GoogleSheet() 

    gs.updateRangeValues(f'Countries!B1:C{len(pizza_values)}' , pizza_values) 
    gs.updateRangeValues(f'Countries!A{len(combine["Беларусь"])+1}:A{len(combine["Беларусь"])+len(combine["Нигерия"])}' , country_value1) 
    gs.updateRangeValues(f'Countries!A1:A{len(combine["Беларусь"])}' , country_value) 
    # gs.service.spreadsheets().values().update(spreadsheetId=gs.SPREADSHEET_ID, range=f'Countries!A1:A{len(combine["Беларусь"])}',valueInputOption='USER_ENTERED', body=test_values) 
    # gs.service.spreadsheets().values().append(spreadsheetId=gs.SPREADSHEET_ID, range=f'Countries!A1:A{len(combine["Беларусь"])}', valueInputOption="USER_ENTERED", body=country_value)
    # gs.service.spreadsheets().values().batchUpdate(spreadsheetId=gs.SPREADSHEET_ID, body=test_values).execute()


    
if __name__== '__main__': 
    main()