from opentelemetry import metrics
from opentelemetry.sdk.metrics import (
    Histogram,
    MeterProvider
)
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    InMemoryMetricReader,
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
