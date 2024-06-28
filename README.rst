Exponential Histogram Issue
===========================

This repo shows how this_ PR fixes its corresponding issue.

0. Clone the ``opentelemetry-python`` repo.
1. Edit ``Pipfile`` so that the path of the ``opentelemetry-*`` packages
   matches the location of the cloned repo.
2. Check out the ``main`` branch in the cloned repo.
3. Run ``pipenv run pytest -vvvv -s``
4. Check out PR ``#3978`` branch (``issue_3977``) in the cloned repo.
5. Run ``pipenv run pytest -vvvv -s``

The issue can be seen in the results of
``test_telemetry.py::test_telemetry_exponential_cumulative``:

When running the tests with ``main``:

::

    test_telemetry.py::test_telemetry_exponential_cumulative 
    start_time_unix_nano:   1719608000933764035
    time_unix_nano:         1719608000933799050
    start_time_unix_nano:   1719608000933764035
    time_unix_nano:         1719608000933873051
    start_time_unix_nano:   1719608000933799050
    time_unix_nano:         1719608000933949137
    start_time_unix_nano:   1719608000933873051
    time_unix_nano:         1719608000934009829
    start_time_unix_nano:   1719608000933949137
    time_unix_nano:         1719608000934067813
    start_time_unix_nano:   1719608000934009829
    time_unix_nano:         1719608000934119026

Notice how the first 2 values of ``start_time_unix_nano`` are the same and they
increase afterwards.

When running thet tests with ``issue_3977``:

::

    test_telemetry.py::test_telemetry_exponential_cumulative 
    start_time_unix_nano:   1719608185445247615
    time_unix_nano:         1719608185445283673
    start_time_unix_nano:   1719608185445247615
    time_unix_nano:         1719608185445370419
    start_time_unix_nano:   1719608185445247615
    time_unix_nano:         1719608185445444918
    start_time_unix_nano:   1719608185445247615
    time_unix_nano:         1719608185445505536
    start_time_unix_nano:   1719608185445247615
    time_unix_nano:         1719608185445564889
    start_time_unix_nano:   1719608185445247615
    time_unix_nano:         1719608185445613709

Notice how the all the values of ``start_time_unix_nano`` remain the same, and
the behavior is consistent with the ``test_telemetry_explicit_*`` test cases
as well.


.. _this: https://github.com/open-telemetry/opentelemetry-python/pull/3978
