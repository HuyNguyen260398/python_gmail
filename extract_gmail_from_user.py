"""
Extract selected mails from your gmail account

1. Make sure you enable IMAP in your gmail settings
(Log on to your Gmail account and go to Settings, See All Settings, and select
Forwarding and POP/IMAP tab. In the "IMAP access" section, select "Enable IMAP")

2. If you have 2-factor authentication, gmail requires you to create an application
sepecific password that you need to use.
Go to your Google account settings and click on "Security"
Scroll down to App Passwords under 2 step verification
Select Mail under Select App. and Other under Select Device. (Give a name, e.g., python)
The system gives you a password that you need to use to authenticate from python
"""

# Import libraries
import imaplib
import email
import yaml

def main():
    with open('credentials.yml') as f:
        content = f.read()

    # From credentials.yaml import user name and password
    creds = yaml.load(content, Loader=yaml.FullLoader)

    # Load the user name and password from yaml file
    user, password = creds['user'], creds['password']

    # URL for IMAP connection
    imap_url = 'imap.gmail.com'

    # Connetion with Gmail using SSL
    mail = imaplib.IMAP4_SSL(imap_url)

    # Log in using credentials
    mail.login(user, password)

    # Select the Inbox to fetch messages
    mail.select('Inbox')

    # Define Key and Value for email search
    # For other keys (criteria): https://gist.github.com/martinrusev/6121028#file-imap-search
    key = 'FROM'
    value = 'prj.ecom.pydj@gmail.com'

    # Search for emails with sepcific key and value
    _, data = mail.search(None, key, value)

    # IDs of all emails that we want to fetch
    mail_id_list = data[0].split()

    # Empty list to capture all messages
    msgs = []

    # Iterate through messages and extract data into the msgs list
    for num in mail_id_list:
        typ, data = mail.fetch(num, '(RFC822)') # RFC822 returns whole message (BODY fetches just body)
        msgs.append(data)

    # Now we have all messages, but with a lot of details
    # List with one item for each part. The easiest way is to walk the message
    # and get the payload on each part:
    # https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python

    # NOTE that a Message object consists of headers and payloads

    # for msg in msgs[::-1]:
    #     for respond_part in msg:
    #         if type(respond_part) is tuple:
    #             my_msg = email.message_from_bytes((respond_part[1]))
    #             print("_________________________________________")
    #             print ("subj:", my_msg['subject'])
    #             print ("from:", my_msg['from'])
    #             print ("body:", my_msg['body'])
                # for part in my_msg.walk():
                #     print(part.get_content_type())
                    # if part.get_content_type() == 'text/plain':
                    #     print(part.get_payload())

    # Debuging - Get 1st mail in email list
    for respond_part in msgs[-1]:
        # print(type(respond_part))
        if type(respond_part) is tuple:
            my_msg = email.message_from_bytes((respond_part[1]))
            # print(type(my_msg))
            print("_________________________________________")
            print("subj:", my_msg['subject'])
            print("from:", my_msg['from'])
            print("body:", my_msg['body'])
            # print("_________________________________________")

if __name__ == '__main__':
    main()