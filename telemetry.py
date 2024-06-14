from opentelemetry import metrics
from opentelemetry.sdk.metrics import (
    Histogram,
    MeterProvider
)
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    ConsoleMetricExporter,
    InMemoryMetricReader,
    PeriodicExportingMetricReader,
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.sdk.metrics.view import View
from opentelemetry.sdk.metrics.view import (
    ExponentialBucketHistogramAggregation
)


class Telemetry:
    def __init__(
        self, target_endpoint="http://localhost:4317/v1/metrics", insecure=True
    ):
        self.in_memory_metric_reader = InMemoryMetricReader(
            preferred_temporality={
                Histogram: AggregationTemporality.CUMULATIVE
            }
        )
        otlp_metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(
                endpoint=target_endpoint,
                insecure=insecure,
                timeout=4,
                preferred_temporality={
                    Histogram: AggregationTemporality.DELTA
                }
            ),
            export_interval_millis=1000
        )
        console_metric_reader = PeriodicExportingMetricReader(
            ConsoleMetricExporter(
                preferred_temporality={Histogram: AggregationTemporality.DELTA}
            ),
            export_interval_millis=10
        )
        otlp_metric_reader
        console_metric_reader
        provider = MeterProvider(
            metric_readers=[self.in_memory_metric_reader],
            views=[
                View(
                    instrument_name="*",
                    aggregation=ExponentialBucketHistogramAggregation()
                )
            ],
        )

        metrics.set_meter_provider(provider)
        meter = metrics.get_meter("pivideo.meter")

        self.frame_latency = meter.create_histogram(
            name="calls",
            unit="ns",
            description="function calls",
        )

    def record_frame_latency(self, latency_ns, **kwargs):
        attributes = {"service.name": "pivideo"}
        attributes.update(**kwargs)
        self.frame_latency.record(latency_ns, attributes)
