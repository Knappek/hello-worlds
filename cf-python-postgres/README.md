# CF App that consumes Postgres Service

1. deploy [VMware Tanzu for Postgres on Cloud Foundry](https://techdocs.broadcom.com/us/en/vmware-tanzu/data-solutions/tanzu-for-postgres-on-cloud-foundry/10-0/postgres/index.html) - a tile in Tanzu Operations Manager
1. create a service in your CF org and space: `cf create-service postgres on-demand-postgres-db python-postgres`
1. push this app that reads and writes data to/from Postgres: `cf push`

## Using the app

Add data (users) to Postgres:

```sh
curl -k -X POST -H "Content-Type: application/json" -d '{"name": "Andy"}' https://<app-url>/user
```

Get the users

```shell
curl -k https://<app-url>/users
```
