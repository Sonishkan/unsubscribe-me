from __future__ import print_function

import os.path

# google gmail api imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# for writing to file
import pandas as pd
import numpy as np
from numpy import array, savetxt


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
        msgs = service.users().messages().list(userId='me', q="unsubscribe").execute()  #### STEP 1
        
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

# Just to print the data to console <<<<<<
#        num = 1
#        for link, sender in zip(unsub_links, email_senders):
#                print('{} {} {}'.format(num, link, sender))
#                num+=1
# >>>>>>>>>>>>
        
        writeFile(unsub_links, email_senders)
        
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

def writeFile(unsubList, senderList):


    a = array(unsubList)
    b = array(senderList)
    
    f = open("unsublist.csv", "w")
    f.write("{},{}\n".format("List-Unsubscribe", "Sender email"))
    for x in zip(a, b):
        f.write("{},{}\n".format(x[0], x[1]))
    f.close()


if __name__ == '__main__':
    main()
