from telemetry import Telemetry
from opentelemetry.sdk.metrics.view import (
    ExponentialBucketHistogramAggregation,
    ExplicitBucketHistogramAggregation
)
from opentelemetry.sdk.metrics.export import AggregationTemporality
from opentelemetry.metrics import _internal as metrics_api
from opentelemetry.util._once import Once
from opentelemetry.metrics._internal import _ProxyMeterProvider
from ipdb import set_trace

set_trace


def reset_metrics_globals() -> None:
    """WARNING: only use this for tests."""
    metrics_api._METER_PROVIDER_SET_ONCE = Once()
    metrics_api._METER_PROVIDER = None
    metrics_api._PROXY_METER_PROVIDER = _ProxyMeterProvider()


def print_times(telemetry):

    print()

    for i in range(6):
        telemetry.histogram.record(i)
        metrics_data = telemetry.in_memory_metric_reader.get_metrics_data()

        start_time_unix_nano = (
            metrics_data.
            resource_metrics[0].
            scope_metrics[0].
            metrics[0].
            data.
            data_points[0].
            start_time_unix_nano
        )
        time_unix_nano = (
            metrics_data.
            resource_metrics[0].
            scope_metrics[0].
            metrics[0].
            data.data_points[0].
            time_unix_nano
        )

        print(f"start_time_unix_nano:\t{start_time_unix_nano}")
        print(f"time_unix_nano:\t\t{time_unix_nano}")

    print()


def test_telemetry_exponential_delta():
    reset_metrics_globals()
    telemetry = Telemetry(
        ExponentialBucketHistogramAggregation(),
        AggregationTemporality.DELTA,
        "exponential_delta_meter",
        "exponential_delta_histogram",
    )

    print_times(telemetry)


def test_telemetry_explicit_delta():
    reset_metrics_globals()
    telemetry = Telemetry(
        ExplicitBucketHistogramAggregation(),
        AggregationTemporality.DELTA,
        "explicit_delta_meter",
        "explicit_delta_histogram"
    )

    print_times(telemetry)


def test_telemetry_exponential_cumulative():
    reset_metrics_globals()
    telemetry = Telemetry(
        ExponentialBucketHistogramAggregation(),
        AggregationTemporality.CUMULATIVE,
        "exponential_cumulative_meter",
        "exponential_cumulative_histogram",
    )

    print_times(telemetry)


def test_telemetry_explicit_cumulative():
    reset_metrics_globals()
    telemetry = Telemetry(
        ExplicitBucketHistogramAggregation(),
        AggregationTemporality.CUMULATIVE,
        "explicit_cumulative_meter",
        "explicit_cumulative_histogram"
    )

    print_times(telemetry)
