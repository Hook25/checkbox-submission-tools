from contextlib import suppress


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
