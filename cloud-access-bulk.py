import requests, json, csv
from oauthlib.oauth2 import TokenExpiredError, Client
from requests_oauthlib import OAuth2Session
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-c", "--csv", action='store', default='cloud-access-data.csv', help="name of the CSV file to read the Cloud Access data from (ccsp;accountNr;nickName)")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-d", "--delete", action='store_true', help="delete all accounts in CSV from Red Hat Cloud Access")
group.add_argument("-a", "--add", action='store_true', help="add all accounts in CSV to Red Hat Cloud Access")
args = parser.parse_args()

# Step 1: we obtain a session token from the openid SSO API, using the offlineToken created
# in the customer portal https://access.redhat.com/management/api
offlineToken = "eyJ.....r0"
client_id = 'rhsm-api'
oauthSession = OAuth2Session(client=Client(client_id=client_id, refresh_token=offlineToken))
openidUrl = 'https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token'
sessionToken = oauthSession.refresh_token(token_url=openidUrl, client_id=client_id)

# Step 2: We use the sessionToken to authenticate our request to add or delete CCSP accounts
# to the registered providers in our Red Hat account using a CSV list like this:
# ccsp;accountNr;nickName
# AWS;123456789012;Project-X
session = requests.Session()
headers = { "Authorization" : "Bearer %s" % (sessionToken['access_token']), "Content-Type" : "application/json" }
with open(args.csv, newline='') as ccspAccounts:
    reader = csv.DictReader(ccspAccounts, delimiter=';')
    for row in reader:
        accountsUrl = 'https://api.access.redhat.com/management/v1/cloud_access_providers/%s/accounts' % (row['ccsp'])
        if args.add:
            print("add %s account #%s (nickname %s)" % (row['ccsp'],row['accountNr'],row['nickName']))
            action = session.post(accountsUrl, headers=headers, json=[{ "id" : row['accountNr'], "nickname" : row['nickName'] }])
        if args.delete:
            print("delete %s account #%s (nickname %s)" % (row['ccsp'],row['accountNr'],row['nickName']))
            action = session.delete(accountsUrl, headers=headers, json={ "id" : row['accountNr'] })


