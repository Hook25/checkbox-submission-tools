import datetime
from contextlib import suppress


def realtime_to_humantime(timestamp_microseconds: int):
    timestamp_seconds = timestamp_microseconds / 1_000_000
    dt_object = datetime.datetime.fromtimestamp(timestamp_seconds, tz=datetime.timezone.utc)
    human_readable_utc = dt_object.strftime("%Y-%m-%d %H:%M:%S UTC")
    return human_readable_utc


def fallback_formatter(formatters: list[str]):
    def _f(x: dict):
        formatters_i = iter(formatters)
        while True:
            try:
                with suppress(KeyError):
                    return next(formatters_i).format(**x)
            except StopIteration:
                raise ValueError(f"Unable to format {str(x)}")

    return _f
