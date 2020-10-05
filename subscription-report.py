import getpass, requests

username=input("Username: ")
password=getpass.getpass("Password for %s:" % username)

session = requests.Session()
session.auth = (username, password)

ownerUrl = 'https://subscription.rhn.redhat.com/subscription/users/%s/owners/' % (username)
owners = session.get(ownerUrl, verify='/etc/rhsm/ca/redhat-uep.pem')

parsed = owners.json()
for owner in parsed :
    ownerKey = owner['key']

entitlementUrl = 'https://subscription.rhn.redhat.com/subscription/owners/%s/entitlements' % (ownerKey)
entitlements = session.get(entitlementUrl)
parsed = entitlements.json()
print('consumer;product;crontract;endDate')
for entitlement in parsed :
    consumer = entitlement['consumer']
    name = consumer['name']
    pool = entitlement['pool']
    contract = pool['contractNumber']
    product = pool['productName']
    endDate = entitlement['endDate']
    # print('consumer %s product %s contract %s endDate %s' % (name,product,contract,endDate))
    print('%s;%s;%s;%s' % (name,product,contract,endDate))

