import requests, json
from oauthlib.oauth2 import TokenExpiredError, Client
from requests_oauthlib import OAuth2Session


# Step 1: we obtain a session token from the openid SSO API, using the offlineToken created
# in the customer portal https://access.redhat.com/management/api
offlineToken = "eyJ.....Er0"
client_id = 'rhsm-api'
oauthSession = OAuth2Session(client=Client(client_id=client_id, refresh_token=offlineToken))
openidUrl = 'https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token'
sessionToken = oauthSession.refresh_token(token_url=openidUrl, client_id=client_id)

# Step 2: We use the sessionToken to authenticate our request to list the currently
# enabled cloud access providers in our Red Hat account
session = requests.Session()
providersUrl = 'https://api.access.redhat.com/management/v1/cloud_access_providers/enabled'
headers = { "Authorization" : "Bearer %s" % (sessionToken['access_token']), "Content-Type" : "application/json" }
providers = session.get(providersUrl, headers=headers)
print(json.dumps(providers.json(), indent=4, sort_keys=True))
