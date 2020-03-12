import requests
import os
from colorama import init
from termcolor import colored
import re
import sys
import json
import argparse
from email_split import email_split

class o365:

    def identify_o365(email_domain):
        email_domain = email_split(open(args.list).readline().rstrip())

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Sec-Fetch-Dest': 'document'
        }

        url_structure = "https://login.microsoftonline.com/{}/.well-known/openid-configuration".format(email_domain.domain)
        r = requests.get(url_structure, headers=headers)
        subscribed = re.search('token_endpoint', r.text)

        # AADSTS90002	InvalidTenantName - The tenant name wasn't found in the data store. Check to make sure you have the correct tenant ID.
        if '"error_codes":[90002]' in r.text: #If not subscribed
            print("The domain isn't using o365")
            exit()

        if subscribed:
            pass


    def enum_company(users):
        users = open(args.list, "r")

        while True:
            line = users.readline()
            if not line:
                break;

            url_schema = "https://login.microsoftonline.com/common/GetCredentialType"
            r = requests.post(url_schema, json={"Username": line.strip()})
#            print(r.text)

            response = r.text
            exists =  re.search('"IfExistsResult":0,', response)
            nonexistent = re.search('"IfExistsResult":1,', response)

            init()

            if exists:
                print(colored(line.strip(), 'blue'))

            if nonexistent:
                print(colored(line.strip(), 'red'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='O365 enum')
    parser.add_argument('-l', '--list', required=True, type=str, help='username list')

    args = parser.parse_args()
    enum = o365()
    enum.identify_o365()
    enum.enum_company()