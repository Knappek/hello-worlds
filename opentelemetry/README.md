# OTel Tracing Hello World

## Send Tracing Data to Jaeger

1. Run Jaeger with Docker:

    ```shell
    docker run -d --name jaeger \
      -e COLLECTOR_OTLP_ENABLED=true \
      -p 16686:16686 \
      -p 4318:4318 \
      jaegertracing/all-in-one:1.54
    ```

1. Open the [Jaeger UI](http://localhost:16686/)
1. Start the Go app and send tracing data to Jaeger:

    ```shell
    export OTEL_SERVICE_NAME=hello-jaeger
    export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
    go run main.go
    ```

1. Make some traffic on your app: [open it in a browser](http://localhost:8080/)
1. you should see traces in Jaeger

## Send Tracing Data to Grafana Cloud via OTLP

1. Navigate to your Grafana Cloud Account at `https://grafana.com/orgs/<your org name>`
1. select your stack (if you have more than one)
1. in `OpenTelemetry` click `Configure`
1. Copy the OTLP endpoint
1. Start the Go app and send tracing data to Jaeger:

    ```shell
    export OTEL_SERVICE_NAME=hello-grafana-cloud
    # export OTEL_EXPORTER_OTLP_ENDPOINT="<your otlp endpoint>", e.g.:
    export OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp-gateway-prod-eu-west-2.grafana.net/otlp"
    go run main.go
    ```

1. Make some traffic on your app: [open it in a browser](http://localhost:8080/)
1. navigate back to your stack in Grafana Cloud
1. `Launch` your Grafana instance
1. Navigate to `Explore` and as the data source select `grafanacloud-<org name>-traces`
1. Click in the `Service Name` value field where you should see the `OTEL_SERVICE_NAME` configured above
1. Click `Run query`
