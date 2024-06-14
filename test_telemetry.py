from telemetry import Telemetry
from ipdb import set_trace


def test_telemetry():
    telemetry = Telemetry()

    print()

    for i in range(5):
        telemetry.record_frame_latency(i, a="b")
        metrics_data = telemetry.in_memory_metric_reader.get_metrics_data()

        print(
            (
                metrics_data.
                resource_metrics[0].
                scope_metrics[0].
                metrics[0].
                data.
                data_points[0].
                start_time_unix_nano,
                metrics_data.
                resource_metrics[0].
                scope_metrics[0].
                metrics[0].
                data.data_points[0].
                time_unix_nano
            )
        )
        print()
