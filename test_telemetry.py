from telemetry import Telemetry
from time import sleep


def test_telemetry():
    telemetry = Telemetry()

    for i in range(10):
        telemetry.record_frame_latency(i, a="b")
        sleep(1)
