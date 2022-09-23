from loguru import logger
from itertools import count
import urllib.request
import json
from GoogleSpreadSheet import GoogleSpreadSheet
import quickstart
import requests



#logger.add(r"Debug\debug{time}.log", format="{time} | {level} | {message}", level="DEBUG", rotation="10 KB", compression="zip")

@logger.catch
def JSONPars (url):
    try:
        with urllib.request.urlopen(url) as URL:
            data = json.load(URL)
        logger.info("Получен ответ в виде json")
        table = {}
        for country in data["countries"]:
            country_name = country["countryName"]
            for pizzeria in country["pizzerias"]:
                table[pizzeria["alias"]] = pizzeria["address"]["locality"]["name"]
        
    except requests.exceptions.InvalidJSONError as ex:
        logger.error(ex)
    except requests.exceptions.RequestException as ex:
        logger.error(ex)
            
            
    output = {
        country_name: table
    }
    
    return output

def main(): 
    try:
        combine = {**JSONPars("https://globalapi.dodopizza.com/api/v1/pizzerias/all/112"), **JSONPars("https://globalapi.dodopizza.com/api/v1/pizzerias/all/566")}
    except Exception as ex:
        logger.error(ex)
    pizza_range = (f'Countries!A1:C{len(combine["Беларусь"])+len(combine["Нигерия"])}')
    pizza_values = [] 
    country_value =[]
    country_value1 =[]
    for value, key in combine["Беларусь"].items(): 
        country_value.append(['Беларусь'])
        pizza_values.append([value,key]) 
    for value, key in combine["Нигерия"].items():
        country_value1.append(['Нигерия'])
        pizza_values.append([value,key]) 

#region OldMethod
    try:
        gs = GoogleSpreadSheet(spreadSheetId = "16mUOHitGZjIwfAGCxwp0WnihellDiWOjBk3GYT8F6g0")
        logger.info("Создан ресурс для взаимодействия с Google API")
    except Exception as ex:
        logger.error(ex)
    try:
        gs.updateRangeValues(f'Countries!B1:C{len(pizza_values)}' , pizza_values) 
        gs.updateRangeValues(f'Countries!A{len(combine["Беларусь"])+1}:A{len(combine["Беларусь"])+len(combine["Нигерия"])}' , country_value1) 
        gs.updateRangeValues(f'Countries!A1:A{len(combine["Беларусь"])}' , country_value)
        logger.info(f"Обновлено: {pizza_range}")
    except Exception as ex:
        logger.error(ex)
#endregion
    
if __name__== '__main__': 
    main()