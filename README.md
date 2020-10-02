# Portal-API
Sample Scripts for the Red Hat Portal API

## Red Hat Portal APIs

Red Hat provides at least two APIs to access the Customer Portal for management of subscriptions, systems, users, cases and alike.

### The RHN API

The old API is introduced in the [Customer Portal Integration Guide](https://access.redhat.com/documentation/en-us/red_hat_customer_portal/1/html/customer_portal_integration_guide)
with additional hints in a [Knowledge Base Article](https://access.redhat.com/solutions/431773)

Even though RHN is shut down, the base URL for this API still has the referrence: `https://subscription.rhn.redhat.com/`


In order to access all the details of your inventory with this old API, you first need to translate your account name to your owner key. The API uses the same certificate CA that is used for the subscription management.
One drawback of the old API is the limitation on basic password authentication.

The following block shows a number of API calls you may want to try:

```
USER=JohnDoe
PASSWD="I'm not going to tell U"
API_URL=https://subscription.rhn.redhat.com/

KEY=$(curl -s --cacert /etc/rhsm/ca/redhat-uep.pem  -u ${USER}:${PASSWD} ${API_URL}/subscription/users/${USER}/owners/ | python3 -mjson.tool|grep key| cut -d'"' -f4)
curl -s --cacert /etc/rhsm/ca/redhat-uep.pem  -u ${USER}:${PASSWD} ${API_URL}/subscription/owners/${KEY}/consumers
curl -s --cacert /etc/rhsm/ca/redhat-uep.pem  -u ${USER}:${PASSWD} ${API_URL}/subscription/owners/${KEY}/products
curl -s --cacert /etc/rhsm/ca/redhat-uep.pem  -u ${USER}:${PASSWD} ${API_URL}/subscription/owners/${KEY}/entitlements
curl -s --cacert /etc/rhsm/ca/redhat-uep.pem  -u ${USER}:${PASSWD} ${API_URL}/subscription/owners/${KEY}/pools
curl -s --cacert /etc/rhsm/ca/redhat-uep.pem  -u ${USER}:${PASSWD} ${API_URL}/subscription/owners/${KEY}/products
curl -s --cacert /etc/rhsm/ca/redhat-uep.pem  -u ${USER}:${PASSWD} ${API_URL}/subscription/owners/${KEY}/activation_keys
```

### The new API

A new API is under development and introduced in another [Knowledge Base Article](https://access.redhat.com/articles/3626371). The entry point to this API is available in the Portal Subscription Management under [Manage->RHSM API Tokens](https://access.redhat.com/management/api). There is an automatic Swagger documentation available for this new API.

This new API allows token based authentication. Unfortunately, it does not provide all the details the old RHN API has. But at least we get the long desired Cloud Access calls.

After generating the offline token for your account in the portal, you first need to call the openid-connect interface to obtain a temporary access token. Then you can try further API calls:

```
OFFLINE_TOKEN='eyJhbGciO....gyOC5wX5Er0'

function jsonValue() {
KEY=$1
num=$2
awk -F"[,:}]" '{for(i=1;i<=NF;i++){if($i~/'$KEY'\042/){print $(i+1)}}}' | tr -d '"' | sed -n ${num}p
}

TOKEN=$(curl https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token -d grant_type=refresh_token -d client_id=rhsm-api -d refresh_token=$offline_token | jsonValue access_token)

curl -s -H "Authorization: Bearer $TOKEN"  "https://api.access.redhat.com/management/v1/systems?limit=100" | python3 -mjson.tool

curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"  --request POST --data '[{"id":"123456789012","nickname":"Project-Y"}]'  "https://api.access.redhat.com/management/v1/cloud_access_providers/AWS/accounts"

curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -X DELETE  --data '{"id":"123456789012"}'  "https://api.access.redhat.com/management/v1/cloud_access_providers/AWS/accounts"
```

There is a nice [RHSM API Client](https://github.com/antonioromito/rhsm-api-client) available for the new API.


## Examples

### Subscription Report
The [subscription-report.py](subscription-report.py) script uses the old API to create a simple CSV report of all registered systems with the contract numbers and expiration dates of their attached subscription entitlements.


