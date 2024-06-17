from opentelemetry import metrics
from opentelemetry.sdk.metrics import (
    Histogram,
    MeterProvider
)
from opentelemetry.sdk.metrics.export import (
    InMemoryMetricReader,
)
from opentelemetry.sdk.metrics.view import View


class Telemetry:
    def __init__(
        self,
        aggregation,
        aggregation_temporality,
        meter_name,
        histogram_name,
    ):
        self.in_memory_metric_reader = InMemoryMetricReader(
            preferred_temporality={
                Histogram: aggregation_temporality
            }
        )
        provider = MeterProvider(
            metric_readers=[self.in_memory_metric_reader],
            views=[
                View(
                    instrument_name="*",
                    aggregation=aggregation
                )
            ],
        )

        metrics.set_meter_provider(provider)
        meter = metrics.get_meter(meter_name)

        self.histogram = meter.create_histogram(
            name=histogram_name
        )

    def record_frame_latency(self, latency_ns, **kwargs):
        attributes = {"service.name": "pivideo"}
        attributes.update(**kwargs)
        self.frame_latency.record(latency_ns, attributes)
