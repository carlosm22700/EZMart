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


def main():
    """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet
    """
    creds = None
    # The file token.json stores user's access and refresh tokens.
    # token.json is created automatically and stored for future use when authorization flow complets for the firs time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no credentials available or if they are invalid, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:  # if credentials are expired
            creds.refresh(Request())  # request to refresh token
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Name, Price, Quantity:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %.2f, %i' % (row[0], float(row[1]), int(row[2])))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
