import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
from http import server
from loguru import logger
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from fastapi import HTTPException


class GoogleSpreadSheet:

    spreadsheetId = None
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def Create_Connection_With_Credentials(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                logger.info('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def __init__(self, **kwargs):
        self.service = build('sheets', 'v4', credentials=self.Create_Connection_With_Credentials())

        if 'spreadSheetId' in kwargs:
            spreadsheet = self.service.spreadsheets().get(spreadsheetId = kwargs['spreadSheetId']).execute()
            
        else:
            spreadsheet = self.service.spreadsheets().create(body = {
            'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                    'sheetId': 0,
                                    'title': 'Лист номер один',
                                    'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
        }).execute()

        self.spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
        print('https://docs.google.com/spreadsheets/d/' + self.spreadsheetId)


    @logger.catch
    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        try:
            result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body=body).execute()
            logger.info('{0} cells updated.'.format(result.get('totalUpdatedCells')))
        except Exception as ex:
            logger.error(ex)
            logger.info(f"{ex} Создан новый лист")
    #         newList = self.service.spreadsheets().create(body = {
    # 'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'}})
    #         try:
    #             self.SPREADSHEET_ID = newList['spreadsheetId'] 
    #         except Exception as ex:
    #             logger.error(ex)
    #         result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body=body).execute()
