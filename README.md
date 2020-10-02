# Portal-API
Sample Scripts for the Red Hat Portal API

## Red Hat Portal APIs

Red Hat provides at least two APIs to access the Customer Portal for management of subscriptions, systems, users, cases and alike.

The old API is introduced in the [Customer Portal Integration Guide](https://access.redhat.com/documentation/en-us/red_hat_customer_portal/1/html/customer_portal_integration_guide)
with additional ints in a [Knowledge Base Article](https://access.redhat.com/solutions/431773)

A new API is under development and introduced in another [Knowledge Base Article](https://access.redhat.com/articles/3626371). The entry point to this API is available in the Portal Subscription Management under [Manage->RHSM API Tokens](https://access.redhat.com/management/api). There is an automatic Swagger documentation available for this new API.

## Examples

### Subscription Report
The [subscription-report.py](subscription-report.py) script uses the old API to create a simple CSV report of all registered systems with the contract numbers and expiration dates of their attached subscription entitlements.


