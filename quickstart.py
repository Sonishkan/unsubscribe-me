from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64 # base64 lib
import re # regex lib

URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)()))"""


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
#            emailbody(service, _id)
            messageheader= service.users().messages().get(userId="me", id=_id, format="full", metadataHeaders=None).execute()
            
            headers = messageheader['payload']['headers']
#            print(headers,'\n\n\n\n\n\n')
            unsub_links.append([i['value'] for i in headers if i["name"]=="List-Unsubscribe"]) ## STEP 2
            email_senders.append([i['value'] for i in headers if i["name"]=="From" or i["name"]=="from"]) ## STEP 2
            
#            print((num_of_messages,'  ', unsub_links[num_of_messages-1],'  ', email_senders[num_of_messages-1]))
            
            #print("\n")
#
        num = 1
        for link, sender in zip(unsub_links, email_senders):
                print('{} {} {}'.format(num, link, sender))
                num+=1
#        print(len(unsub_links))
        unsub_links = list(filter(None, unsub_links))
        email_senders = list(filter(None, email_senders))
#        print(len(unsub_links))
#        print(len(email_senders))
        print("num of messages: ", num_of_messages)
        print("num of unsub list: ", len(unsub_links))
        print("num of sender emails: ", len(email_senders))
        
        

    # print(messageheader)
        
        
        

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

## method to get all emails with unsubscribe/optout... in the header and the body

## method to get the unsub link from email and save to csv file

def emailbody(service, _id):
    msg = service.users().messages().get(userId='me', id=_id).execute()
    payld = msg['payload']
    if 'parts' in payld:
        mssg_parts = payld['parts']  # fetching the message parts
        part_one = mssg_parts[0]  # fetching first element of the part
        part_body = part_one['body']  # fetching body of the message
        if 'data' in part_body:
            part_data = part_body['data']  # fetching data from the body
            # decoding from Base64 to UTF-8
            clean_one = part_data.replace("-", "+")
            # decoding from Base64 to UTF-8
            clean_one = clean_one.replace("_", "/")
            # decoding from Base64 to UTF-8
            clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))
            values = re.findall(URL_REGEX, str(clean_two))
            for val in values:
                if 'unsubscribe'  in val[0]:
                    print(val[0]+'/n')

def getLabels():
        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

def getMetadata():
        service.users.messages.getMetadata.list(userId='me').execute()

def getMostreplies():
        threads = service.users().threads().list(userId='me').execute().get('threads', [])
        for thread in threads:
            tdata = service.users().threads().get(userId='me', id=thread['id']).execute()
            nmsgs = len(tdata['messages'])

            # skip if <3 msgs in thread
            if nmsgs > 1:
                msg = tdata['messages'][0]['payload']
                subject = ''
                for header in msg['headers']:
                    if header['name'] == 'Subject':
                        subject = header['value']
                        break
                if subject:  # skip if no Subject line
                    print(F'- {subject}, {nmsgs}')
        return threads











if __name__ == '__main__':
    main()
