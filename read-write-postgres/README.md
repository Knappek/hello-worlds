# Go App that uses PostgreSQL

This is a simple Go Web Application that writes data to an external PostgreSQL server and displays the data.

## Prerequisites

- PostgreSQL server Uri

## Start the App

1. download all dependencies: `go mod tidy`
1. run the app: `go run main.go`
1. access the app: [http://localhost:8080](http://localhost:8080)

## Access PostgreSQL without SSL

Use the Postgres Uri `postgresql://pgadmin:6UE1k78239Oi0pv45PsD@tcp.172.30.7.140.nip.io:18000/postgres?sslmode=disable` instead of `postgresql://pgadmin:6UE1k78239Oi0pv45PsD@tcp.172.30.7.140.nip.io:18000/postgres`.
