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
print('consumer;contract;endDate')
for entitlement in parsed :
    consumer = entitlement['consumer']
    name = consumer['name']
    pool = entitlement['pool']
    contract = pool['contractNumber']
    endDate = entitlement['endDate']
    # print('consumer %s contract %s endDate %s' % (name,contract,endDate))
    print('%s;%s;%s' % (name,contract,endDate))

