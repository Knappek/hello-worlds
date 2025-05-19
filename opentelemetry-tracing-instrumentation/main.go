package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
)

func main() {
	// Setup OpenTelemetry
	tp, err := setupTracerProvider()
	if err != nil {
		log.Fatalf("failed to initialize tracer provider: %v", err)
	}
	defer func() { _ = tp.Shutdown(context.Background()) }()

	tracer := otel.Tracer("hello-world-tracer")

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		ctx, span := tracer.Start(r.Context(), "helloHandler")
		defer span.End()

		span.SetAttributes(attribute.String("custom.attribute", "hello-world"))

		fmt.Fprintln(w, "Hello, World!")
		log.Println("Handled request")

		doWork(ctx)
	})

	log.Println("Starting server on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func setupTracerProvider() (*sdktrace.TracerProvider, error) {
	ctx := context.Background()

	exporter, err := otlptracehttp.New(ctx)
	if err != nil {
		return nil, err
	}

	// Automatically detect service name from OTEL_SERVICE_NAME and other env vars
	res, err := resource.New(ctx,
		resource.WithFromEnv(),      // Load OTEL_* env vars
		resource.WithProcess(),      // Info about the current process
		resource.WithTelemetrySDK(), // SDK info
		resource.WithHost(),         // Host info
		resource.WithAttributes(),   // Add custom attributes here if needed
	)
	if err != nil {
		return nil, err
	}

	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exporter),
		sdktrace.WithResource(res),
	)

	otel.SetTracerProvider(tp)
	return tp, nil
}

func doWork(ctx context.Context) {
	tracer := otel.Tracer("hello-world-tracer")
	_, span := tracer.Start(ctx, "doWork")
	defer span.End()

	log.Println("Doing some work...")
}

