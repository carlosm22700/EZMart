'''
This file contains services related to fetching and working with GOOGLE APIs
'''

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet
SAMPLE_SPREADSHEET_ID = '1BTHmikgF9gkPdyUU8MQgFrxyoWQDmBkpDloNfor_-a4'
SAMPLE_RANGE_NAME = 'Fruit Data!A2:C'
CREDENTIALS_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'credentials.json')

'''
Todo:

1)Refactor code:
turn main into a class?
class would contain functions: check_auth and fetch_data so that fetch_data can just call on check_auth. and we can just call on fetch_data in my views. so that the view takes care of storing the data and the crud functionality for its model?

2)create view to save data to db
'''


# def main():
#     """
#     Shows basic usage of the Sheets API.
#     Prints values from a sample spreadsheet
#     """
#     creds = None
#     # The file token.json stores user's access and refresh tokens.
#     # token.json is created automatically and stored for future use when authorization flow complets for the firs time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no credentials available or if they are invalid, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:  # if credentials are expired
#             creds.refresh(Request())  # request to refresh token
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 CREDENTIALS_PATH, SCOPES)
#             creds = flow.run_local_server(port=8080)
#         # Save the credentials for next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     try:
#         service = build('sheets', 'v4', credentials=creds)

#         # Call the Sheets API
#         sheet = service.spreadsheets()
#         result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                     range=SAMPLE_RANGE_NAME).execute()
#         values = result.get('values', [])

#         if not values:
#             print('No data found.')
#             return

#         print('Name, Price, Quantity:')
#         for row in values:
#             # Print columns A and E, which correspond to indices 0 and 4.
#             print('%s, %.2f, %i' % (row[0], float(row[1]), int(row[2])))

#             sheet_data = '%s, %.2f, %i' % (row[0], float(row[1]), int(row[2]))

#             return sheet_data
#     except HttpError as err:
#         print(err)


# if __name__ == '__main__':
#     main()


'''
the following is slightly slower but better structured
'''


class GoogleSheetService:
    '''
    Service class for Google Sheets API interactions.
    '''

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SAMPLE_SPREADSHEET_ID = '1BTHmikgF9gkPdyUU8MQgFrxyoWQDmBkpDloNfor_-a4'
    SAMPLE_RANGE_NAME = 'Fruit Data!A2:C'
    CREDENTIALS_PATH = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'credentials.json')

    def __init__(self):
        self.creds = None
        self.service = None

    def check_auth(self):
        '''
        Check if the user is authenticated and perform authentication if needed.
        '''
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file(
                'token.json', self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_PATH, self.SCOPES)
                self.creds = flow.run_local_server(port=8080)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def fetch_data(self):
        '''
        Fetch data from the Google Sheet.
        '''
        self.check_auth()
        self.service = build('sheets', 'v4', credentials=self.creds)
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                                    range=self.SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        data_list = []
        for row in values:
            data = {
                'Name': row[0],
                'Price': float(row[1]),
                'Quantity': int(row[2])
            }
            data_list.append(data)

        return data_list


if __name__ == '__main__':
    '''
    Main entry point of the script.
    '''
    service = GoogleSheetService()
    data = service.fetch_data()
    for item in data:
        print('Name: {}, Price: {:.2f}, Quantity: {}'.format(
            item['Name'], item['Price'], item['Quantity']))
