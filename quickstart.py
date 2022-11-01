from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        threads = service.users().threads().list(userId='me').execute().get('threads', [])
        message = threads[0].get('id')
        #print(message)
        msgs = service.users().messages().list(userId='me', q="unsubscribe").execute()  #### STEP 1
        
        # find all emails with unsubscribe in the messsage
            # find all message that have headers of Lis-Unsubscribe
            # find all email addresses of senders
#        print(len(msgs))
        
        unsub_links = []
        email_senders=[]
        

        num_of_messages = 0
        for msg in msgs['messages']:
            num_of_messages+=1
            _id = msg['id']
#            print(_id)
            messageheader= service.users().messages().get(userId="me", id=_id, format="full", metadataHeaders=None).execute()
            
            headers = messageheader['payload']['headers']
#            print(headers,'\n\n\n\n\n\n')
            unsub_links.append([i['value'] for i in headers if i["name"]=="List-Unsubscribe"]) ## STEP 2
            email_senders.append([i['value'] for i in headers if i["name"]=="From" or i["name"]=="from"]) ## STEP 2

        num = 1
        for link, sender in zip(unsub_links, email_senders):
                print('{} {} {}'.format(num, link, sender))
                num+=1

        unsub_links = list(filter(None, unsub_links))
        email_senders = list(filter(None, email_senders))

        print("num of messages: ", num_of_messages)
        print("num of unsub list: ", len(unsub_links))
        print("num of sender emails: ", len(email_senders))


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

## method to get all emails with unsubscribe/optout... in the header and the body

## method to get the unsub link from email and save to csv file


if __name__ == '__main__':
    main()
